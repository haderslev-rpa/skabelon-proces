from automation_server_client import AutomationServer
from Test2.haderlev_vbo import update_item_data


def process_item(item):
    with item:
        data = item.data or {}

        update_item_data(
            data,
            item=item,
            persist=True,
            data_updates={              # 🔴 DEN RIGTIGE NØGLE
                "process_result": {
                    "status": "OK"
                }
            }
        )


if __name__ == "__main__":
    ats = AutomationServer.from_environment()
    for item in ats.workqueue():
        process_item(item)