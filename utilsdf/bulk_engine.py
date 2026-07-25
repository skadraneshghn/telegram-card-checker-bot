import asyncio
import time
import traceback
from typing import List, Dict, Any
from pyrogram import Client
from utilsdf.gate_registry import get_all_gateways
from utilsdf.logger import logger
from utilsdf.db import Database


class BulkTask:
    def __init__(self, task_id: str, client: Client, user_id: int, chat_id: int, gate_cmd: str, cards: List[tuple]):
        self.task_id = task_id
        self.client = client
        self.user_id = user_id
        self.chat_id = chat_id
        self.gate_cmd = gate_cmd
        self.cards = cards
        self.total = len(cards)
        self.queue: asyncio.Queue = asyncio.Queue()
        self.processed = 0
        self.approved = 0
        self.declined = 0
        self.errors = 0
        self.start_time = time.time()
        self.status_msg = None
        self.is_running = True

        # Populate FIFO Queue
        for card in cards:
            self.queue.put_nowait(card)


active_bulk_tasks: Dict[str, BulkTask] = {}


async def run_bulk_checker_task(client: Client, user_id: int, chat_id: int, gate_cmd: str, cards: List[tuple]):
    """
    Spawns and executes a FIFO bulk card processing task.
    """
    gateways = get_all_gateways()
    gate_info = gateways.get(gate_cmd)
    if not gate_info:
        return await client.send_message(chat_id, "<b>❌ Selected gateway is not available.</b>")

    task_id = f"blk_{user_id}_{int(time.time())}"
    task = BulkTask(task_id, client, user_id, chat_id, gate_cmd, cards)
    active_bulk_tasks[task_id] = task

    gate_name = gate_info["name"]
    gate_func = gate_info["func"]
    gate_type = gate_info.get("type", "tuple")

    # Send initial status message
    initial_text = f"""<b>🚀 𝘽𝙪𝙡𝙠 𝘾𝙝𝙚𝙘𝙠 𝙞𝙣 𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨 »</b>

<b>🔹 Gate -»</b> <code>{gate_name}</code>
<b>🔹 Progress -»</b> <code>[0/{task.total}] (0%)</code>
<b>✅ Approved -»</b> <code>0</code>
<b>❌ Declined -»</b> <code>0</code>
<b>⏳ Remaining in Queue -»</b> <code>{task.total}</code>"""

    try:
        task.status_msg = await client.send_message(chat_id, initial_text)
    except Exception as e:
        logger.error(f"Failed to send initial status message: {e}")

    logger.info(f"Started Bulk FIFO Task [{task_id}] for User [{user_id}] on Gate [{gate_name}] with {task.total} cards.")

    # Worker processing loop (FIFO)
    while not task.queue.empty():
        card_tuple = await task.queue.get()
        cc, month, year, cvv = card_tuple
        cc_formatted = f"{cc}|{month}|{year}|{cvv}"

        status_str = "Dead! ❌"
        result_str = "Unknown"
        is_live = False

        try:
            res = await gate_func(cc, month, year, cvv)
            if gate_type == "dict" and isinstance(res, dict):
                resp_text = res.get("response", "Unavailable")
                status_raw = res.get("status", "UNAVAILABLE")
                result_str = resp_text
                if "APPROVED" in status_raw.upper() or "APPROVED" in resp_text.upper() or "THANK YOU" in resp_text.upper():
                    status_str = "Approved! ✅"
                    is_live = True
                else:
                    status_str = "Dead! ❌"
            elif gate_type == "tuple" and isinstance(res, tuple) and len(res) >= 2:
                status_raw, resp_raw = res[0], res[1]
                result_str = str(resp_raw)
                if "APPROVED" in str(status_raw).upper() or "LIVE" in str(status_raw).upper():
                    status_str = "Approved! ✅"
                    is_live = True
                else:
                    status_str = "Dead! ❌"
            elif isinstance(res, str):
                result_str = res
                if "APPROVED" in res.upper() or "THANK YOU" in res.upper():
                    status_str = "Approved! ✅"
                    is_live = True
                else:
                    status_str = "Dead! ❌"
            else:
                result_str = str(res)
        except Exception as e:
            traceback.print_exc()
            task.errors += 1
            status_str = "Error! ❌"
            result_str = f"{type(e).__name__}: {str(e)[:50]}"

        task.processed += 1
        if is_live:
            task.approved += 1
        else:
            task.declined += 1

        # Log check to DB
        try:
            with Database() as db:
                db.increase_checks(user_id)
        except Exception:
            pass

        # Send individual card result message to Telegram
        card_res_text = f"""<b>🔹 𝘽𝙪𝙡𝙠 𝘾𝘾 -» <code>{cc_formatted}</code>
🔹 𝙎𝙩𝙖𝙩𝙪𝙨 -» <code>{status_str}</code>
🔹 𝙍𝙚𝙨𝙪𝙡𝙩 -» <code>{result_str}</code>
🔹 𝙂𝙖𝙩𝙚𝙬𝙖𝙮 -» <code>{gate_name}</code></b>"""

        try:
            await client.send_message(chat_id, card_res_text)
        except Exception as e:
            logger.error(f"Failed to send card result for {cc_formatted}: {e}")

        # Update dashboard message every 3 cards or on last item
        remaining = task.total - task.processed
        pct = int((task.processed / task.total) * 100)
        
        if task.processed % 3 == 0 or remaining == 0:
            updated_dashboard = f"""<b>🚀 𝘽𝙪𝙡𝙠 𝘾𝙝𝙚𝙘𝙠 𝙞𝙣 𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨 »</b>

<b>🔹 Gate -»</b> <code>{gate_name}</code>
<b>🔹 Progress -»</b> <code>[{task.processed}/{task.total}] ({pct}%)</code>
<b>✅ Approved -»</b> <code>{task.approved}</code>
<b>❌ Declined -»</b> <code>{task.declined}</code>
<b>⏳ Remaining in Queue -»</b> <code>{remaining}</code>"""
            try:
                if task.status_msg:
                    await task.status_msg.edit_text(updated_dashboard)
            except Exception:
                pass

        task.queue.task_done()
        await asyncio.sleep(1)  # 1 second rate-limit gap between cards

    # Task Completion Summary Report
    elapsed = round(time.time() - task.start_time, 2)
    final_report = f"""<b>🏁 𝘽𝙪𝙡𝙠 𝘾𝙝𝙚𝙘𝙠 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙!</b>

<b>🔹 Gate -»</b> <code>{gate_name}</code>
<b>🔹 Total Checked -»</b> <code>{task.total}</code>
<b>✅ Approved -»</b> <code>{task.approved}</code>
<b>❌ Declined -»</b> <code>{task.declined}</code>
<b>⚠️ Errors -»</b> <code>{task.errors}</code>
<b>⏱ Total Time -»</b> <code>{elapsed}s</code>"""

    try:
        await client.send_message(chat_id, final_report)
    except Exception as e:
        logger.error(f"Failed to send final bulk report: {e}")

    active_bulk_tasks.pop(task_id, None)
