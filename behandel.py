
def behandel_page(item):
    print("Nu kører koden i behandl.py")
    data = item.data

    from q_haderslev_vbo.automation_server.ats_update_item_data import update_item_data

    update_item_data(
        data,
        state="INDSÆT State fx Brev sendt",
        item=item
    )              