def behandel_page(item, session, page):

    from q_haderslev_vbo.automation_server.ats_update_item_data import update_item_data
    from q_haderslev_vbo.automation_server.ats_find_state import find_state
    import logging
    logger = logging.getLogger(__name__)

    data = item.data

    """
    PLAYWRIGHT – NY STANDARD (VIGTIGT):

    - BrowserSession (objekt – browser-livscyklus) oprettes i main.py
    - session gives IND i behandel_page som parameter
    - behandel_page må:
        ✅ bruge page.goto() (funktion – navigér)
        ✅ tage screenshots via await session.recorder.screenshot(page,"cura_efter_login",always=True)
        ✅ tage optage video via await session.recorder.start_recording(page, 10)
    - behandel_page må IKKE:
        ❌ oprette BrowserSession
        ❌ lukke session eller browser 
        ❌ bruge session.new_page() (funktion – ny fane) (kan godt være undtagelser)
        ❌ have try/except/finally for Playwright

    Exception-håndtering, screenshots ved fejl og session.close()
    håndteres ALTID i main.py.
    """

    # ==========================================================
    # 🧠 STATES
    # ==========================================================
    class States:
        SEND_BREV = "1.0 Brev sendt"
        JOURNALISER_BREV = "1.5 Brev journaliseret"
        AFSLUT_SAG = "2.0 Sag afsluttet"


    # ==========================================================
    # 🔁 HELPERS
    # ==========================================================
    def har_state(state):
        return find_state(data, search_text=state)

    def mangler_state(state):
        return not har_state(state)

    def set_state(state):
        update_item_data(data, item=item, state=state)

    def log_step(step, text):
        logger.info(f"[{step}] {text}")


    # ==========================================================
    step = "SEND_BREV"
    # ==========================================================
    state = getattr(States, step)

    if mangler_state(state):

        log_step(step, "Start")

        data["box"]["brev_sendt_id"] = 123
        log_step(step, f'ID sat: {data["box"]["brev_sendt_id"]}')

        update_item_data(data, item=item)

        set_state(state)


    # ==========================================================
    step = "JOURNALISER_BREV"
    # ==========================================================
    state = getattr(States, step)

    if mangler_state(state):

        log_step(step, "Start")

        data["box"]["journal_id"] = 456
        log_step(step, f'ID sat: {data["box"]["journal_id"]}')

        update_item_data(data, item=item)

        set_state(state)


    # ==========================================================
    step = "AFSLUT_SAG"
    # ==========================================================
    state = getattr(States, step)

    if mangler_state(state):

        log_step(step, "Start")

        data["box"]["afslutnings_id"] = 789
        log_step(step, f'ID sat: {data["box"]["afslutnings_id"]}')

        update_item_data(data, item=item)

        set_state(state)
