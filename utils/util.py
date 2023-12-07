
import fitz
from constants import light_red_color, light_blue_color, light_green_color, light_orange_color


def extract_menu_items(mandalay_bay_beo_pdf):
    # doc = fitz.open(mandalay_bay_beo_pdf)
    doc = fitz.open("pdf", mandalay_bay_beo_pdf)
    menu_items = ""
    for page in doc:
        tables = page.find_tables()
        # print(f"{len(tables.tables)} table(s) on {page}")
        for table in tables:
            for cell in table.extract():
                # I assume there will be at least 1 $ symbol in the cell that has a Menu item
                if any('$' in x for x in cell):
                    for item in cell:
                        menu_items += item
    print("Menu items extract from pdf is\n" + menu_items)
    return menu_items


def color_code_menu_items(mandalay_bay_beo_pdf, recommend_kitchen_zone_map):
    def legends():
        page.clean_contents()
        pos_t = (500, 80)
        for zone in ["For Hot Kitchen", "For Cold Kitchen", "For Baking", "For Beverage"]:
            tw = fitz.TextWriter(page.rect)
            tw.append(pos_t, zone, small_caps=True)
            tw.write_text(page)
            for r in page.search_for(zone):
                highlight = page.add_highlight_annot(r)
                if 'hot' in zone.lower():
                    highlight.set_colors(stroke=light_red_color)
                if 'cold' in zone.lower():
                    highlight.set_colors(stroke=light_blue_color)
                if 'baking' in zone.lower():
                    highlight.set_colors(stroke=light_green_color)
                if 'beverage' in zone.lower():
                    highlight.set_colors(stroke=light_orange_color)
                highlight.update()
            # Updating tuple - immutable hence the list conversion step
            pos_l = list(pos_t)
            pos_l[1] += 20
            pos_t = tuple(pos_l)

    def custom_highlight(zone):
        if 'hot' in zone.lower():
            highlight.set_colors(stroke=light_red_color)
        if 'cold' in zone.lower():
            highlight.set_colors(stroke=light_blue_color)
        if 'baking' in zone.lower():
            highlight.set_colors(stroke=light_green_color)
        if 'beverage' in zone.lower():
            highlight.set_colors(stroke=light_orange_color)
        highlight.update()

    # doc = fitz.open(mandalay_bay_beo_pdf)
    doc = fitz.open("pdf", mandalay_bay_beo_pdf)
    for page in doc:
        # recommend_kitchen_zone_list = ast.literal_eval(recommend_kitchen_zone_map)
        # recommend_kitchen_zone_list = [n.strip() for n in recommend_kitchen_zone_list]
        # for item in recommend_kitchen_zone_list:
        #     if 'Italian' in item:
        #         item = 'Mini Italian Sausage Calzones with Sweet Basil-'
        #     for r in page.search_for(item):
        #         highlight = page.add_highlight_annot(r)
        for zone in recommend_kitchen_zone_map:
            # if not isinstance(recommend_kitchen_zone_map[zone], str):
            for item in recommend_kitchen_zone_map[zone]:
                for r in page.search_for(item):
                    if 'other' not in zone.lower():
                        highlight = page.add_highlight_annot(r)
                        custom_highlight(zone)
            # else:
            #     for item, category in recommend_kitchen_zone_map.items():
            #         for r in page.search_for(item):
            #             if 'other' not in category:
            #                 highlight = page.add_highlight_annot(r)
            #                 custom_highlight(category)
            #     break
        legends()
    return doc.tobytes()
