import json
from automation_server_client import AutomationServer
from Test2.haderlev_vbo import update_item_data


def process_item(item):
    """
    Kører ét work item og returnerer det endelige JSON,
    uanset om persistence virker eller ej.
    """

    with item:
        # HENT JSON ÉN GANG
        data_json = item.data or {}

        # ---------- TRIN 1 ----------
        update_item_data(
            data_json,
            item=item,
            persist=True, 
            state_updates={"trin_1": "AFSLUTTET"},
            log_entry={"step": "1.0 Trin 1", "result": "OK"},
        )

        # ---------- TRIN 2 ----------
        update_item_data(
            data_json,
            state_updates={"trin_2": "AFSLUTTET"},
            log_entry={"step": "2.0 Trin 2", "result": "OK"},
        )

        # ---------- TRIN 3 – BESLUTNING ----------
        borger_udenfor_scope = True  # simulerer logik

        if borger_udenfor_scope:
            update_item_data(
                data_json,
                status_updates={
                    "status": "MANUEL",
                    "status_kode": "BORGER_UDENFOR_SCOPE",
                },
                log_entry={
                    "step": "3.0 Trin 3",
                    "result": "MANUEL",
                    "note": "Borger udenfor målgruppen",
                },
            )

            # 🔴 MEGET VIGTIGT
            # Returnér JSON'en så main kan printe den
            return data_json

        # ---------- TRIN 4 ----------
        update_item_data(
            data_json,
            state_updates={"trin_4": "AFSLUTTET"},
            log_entry={"step": "4.0 Trin 4", "result": "OK"},
        )

        # ---------- TRIN 5 – AFSLUT ----------
        update_item_data(
            data_json,
            status_updates={"status": "COMPLETED"},
            log_entry={"step": "5.0 Afsluttet", "result": "OK"},
        )

        return data_json


def pretty_print(title: str, data: dict):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("=" * 80 + "\n")


if __name__ == "__main__":
    ats = AutomationServer.from_environment()
    workqueue = ats.workqueue()

    for item in workqueue:
        result_json = process_item(item)

        # ✅ HER SER DU RESULTATET,
        # uanset om Automation Server gemmer eller ej
        pretty_print(
            f"RESULTAT FOR ITEM (id={item.id})",
            result_json
        )