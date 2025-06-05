def build_complete_menu(menu_id, menu_label, button_items, submenu_items=None):
    """Builds a complete floating menu with given buttons and submenus."""
    def build_menu_button(label, button_id):
        return f'''
        <div class="menu_option">
          <button class="menu_link" id="{button_id}">{label}</button>
        </div>
        '''

    def build_menu_submenu(label, button_map):
        submenu = '\n'.join(
            f'<button class="menu_link_tab" id="{bid}">{blabel}</button>'
            for bid, blabel in button_map.items()
        )
        return f'''
        <div class="menu_option has-children">
          <span>{label}</span>
          <div class="menu_submenu">
            {submenu}
          </div>
        </div>
        '''

    sections = []
    for label, bid in button_items:
        sections.append(build_menu_button(label, bid))

    if submenu_items:
        for submenu in submenu_items:
            sections.append(build_menu_submenu(submenu["label"], submenu["buttons"]))

    return f'''
<div id="float-{menu_id}-container" class="float_menu">
  <span class="menu_label">{menu_label}</span>
  <div class="menu_dropdown_container" id="{menu_id}-dropdown">
    {''.join(sections)}
  </div>
</div>
'''
