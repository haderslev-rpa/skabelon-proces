from automation_server_client import AutomationServer
from Test2.haderlev_vbo import update_item_data


def process_item(item):
    """
    Dette svarer til én kørsel af et work item
    """

    # --- HENT JSON ÉN GANG ---
    with item:
        data_json = item.data or {}

        # ----- TRIN 1 -----
        update_item_data(
            data_json,
            item=item,
            persist=True,  
            state_updates={
                "trin_1": "AFSLUTTET"
            },
            log_entry={
                "step": "1.0 Trin 1",
                "result": "OK"
            }
        )

        # ----- TRIN 2 -----
        update_item_data(
            data_json,
            state_updates={
                "trin_2": "AFSLUTTET"
            },
            log_entry={
                "step": "2.0 Trin 2",
                "result": "OK"
            }
        )

        # ----- TRIN 3 — BESLUTNING -----
        borger_udenfor_scope = True  # simuleret decision

        if borger_udenfor_scope:
            # --- MANUEL STOP ---
            update_item_data(
                data_json,
                status_updates={
                    "status": "MANUEL",
                    "status_kode": "BORGER_UDENFOR_SCOPE"
                },
                log_entry={
                    "step": "3.0 Trin 3",
                    "result": "MANUEL",
                    "note": "Borger udenfor målgruppen"
                }
)


            # ✅ VIGTIGT:
            # Ingen item.complete() her
            # with-blokken sørger selv for at complete item
            return

        # ----- TRIN 4 -----
        update_item_data(
            data_json,
            state_updates={
                "trin_4": "AFSLUTTET"
            },
            log_entry={
                "step": "4.0 Trin 4",
                "result": "OK"
            }
        )

        # ----- TRIN 5 – FÆRDIG -----
        update_item_data(
            data_json,
            status_updates={
                "status": "COMPLETED"
            },
            log_entry={
                "step": "5.0 Afsluttet",
                "result": "OK"
            },
            item=item,
            persist=True
        )

        # ✅ Ingen item.complete() her heller
        # with-blokken afslutter item automatisk


if __name__ == "__main__":
    ats = AutomationServer.from_environment()
    workqueue = ats.workqueue()

    for item in workqueue:
        process_item(item)