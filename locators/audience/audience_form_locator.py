from selenium.webdriver.common.by import Byclass AudienceFormLocators:    # [Start] locators    save_button_locator = (By.XPATH, "//button[text()='Save' and @type='submit']")    cancel_button_locator = (By.XPATH, "//button[text()='CANCEL' and @type='reset']")    add_button_locator = (By.XPATH, "//button[@data-role='add']")    selected_first_item_locator = (By.XPATH, "//select[@class='form-control native-select' and @name='[]']//option")    csv_file_upload_locator = (By.XPATH, "//input[@name='csv']")    remove_if_url_contains_field_locator = (By.XPATH, "//label[normalize-space()='Remove if URL contains:']/..//input")    # [End] locators    # [Start] Label names    name_field_name = "Name:"    description_field_name = "Description:"    type_field_name = "Type:"    country_field_name = "Country:"    country_form_field_name = "Country"    audience_list_field_name = "Audience list"    users_field_name = "Users"    date_field_name = "Date"    rule_field_name = "Rule:"    method_field_name = "Method"    user_validity_field_name = "User validity"    exchange_field_name = "Exchange"    type_form_field_name = "Type"    generate_insights_report_field_name = "Generate insights report"    # [End] Label names    # [Start] Attribute values    audience_field_name = "name"    description1_id = "description1"    type_container_id = "select2-js-type-container"    country_container_id = "select2-js-country-container"    verticals_id = "verticals"    form_control_class = "form-control"    user_validity_minutes_id = "user_validity_minutes"    select2_validity_type_container_id = "select2-validity_type-container"    select2_generate_insight_form_container_id = "select2-generate_insight_form-container"    amount_locations_id = "amount-locations"    select2_selection_choice_class = "select2-selection__choice"    # [End] Attribute values