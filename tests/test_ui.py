"""
UI smoke tests using Playwright.

Prerequisites:
    pip install pytest-playwright
    playwright install chromium

Run:
    python -m pytest tests/test_ui.py -v --headed   # see browser
    python -m pytest tests/test_ui.py -v            # headless

These tests expect the frontend to be served at http://127.0.0.1:3000.
Start the dev server first:  python dev.py
"""

import pytest
from playwright.sync_api import Page, expect


BASE = "http://127.0.0.1:3000"


# ── Landing page ──────────────────────────────────────────────────────────────

class TestLandingPage:
    def test_title_contains_anaida(self, page: Page):
        page.goto(BASE)
        expect(page).to_have_title("Anaida Space")

    def test_hero_heading_visible(self, page: Page):
        page.goto(BASE)
        hero = page.locator("h1").first
        expect(hero).to_be_visible()

    def test_nav_links_present(self, page: Page):
        page.goto(BASE)
        nav = page.locator("nav")
        expect(nav).to_be_visible()

    def test_cta_button_present(self, page: Page):
        page.goto(BASE)
        btn = page.locator("a[href='registration.html'], a[href='dashboard.html']").first
        expect(btn).to_be_visible()


# ── Registration page ─────────────────────────────────────────────────────────

class TestRegistrationPage:
    def test_page_loads(self, page: Page):
        page.goto(f"{BASE}/registration.html")
        expect(page).not_to_have_title("")

    def test_email_field_present(self, page: Page):
        page.goto(f"{BASE}/registration.html")
        expect(page.locator("input[type='email'], input[name='email'], #email")).to_be_visible()

    def test_password_field_present(self, page: Page):
        page.goto(f"{BASE}/registration.html")
        expect(page.locator("input[type='password']").first).to_be_visible()

    def test_submit_button_present(self, page: Page):
        page.goto(f"{BASE}/registration.html")
        submit = page.locator("button[type='submit'], .btn").first
        expect(submit).to_be_visible()


# ── Dashboard page ────────────────────────────────────────────────────────────

class TestDashboardPage:
    def test_page_loads(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        expect(page).to_have_title("Dashboard — Anaida Space")

    def test_nav_tabs_visible(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        tabs = page.locator(".dash-tab")
        expect(tabs.first).to_be_visible()

    def test_overview_tab_active_by_default(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        overview_tab = page.locator(".dash-tab[data-panel='overview']")
        expect(overview_tab).to_have_class("dash-tab active")

    def test_overview_panel_visible(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        panel = page.locator("#panel-overview")
        expect(panel).to_be_visible()

    def test_tab_switching_protocol(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='protocol']").click()
        expect(page.locator("#panel-protocol")).to_be_visible()
        expect(page.locator("#panel-overview")).not_to_be_visible()

    def test_tab_switching_program(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='program']").click()
        expect(page.locator("#panel-program")).to_be_visible()

    def test_tab_switching_review(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='review']").click()
        expect(page.locator("#panel-review")).to_be_visible()

    def test_tab_switching_productivity(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='productivity']").click()
        expect(page.locator("#panel-productivity")).to_be_visible()

    def test_tab_switching_study(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='study']").click()
        expect(page.locator("#panel-study")).to_be_visible()

    def test_tab_switching_rewards(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='rewards']").click()
        expect(page.locator("#panel-rewards")).to_be_visible()

    def test_tab_switching_chat(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='chat']").click()
        expect(page.locator("#panel-chat")).to_be_visible()

    def test_all_eight_tabs_exist(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        expected = ["overview", "protocol", "program", "review",
                    "productivity", "study", "rewards", "chat"]
        for name in expected:
            tab = page.locator(f".dash-tab[data-panel='{name}']")
            expect(tab).to_be_visible()

    def test_protocol_create_form_visible_when_logged_out(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='protocol']").click()
        create_btn = page.locator("#protocolCreateBtn")
        expect(create_btn).to_be_visible()

    def test_program_start_form_visible(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='program']").click()
        btn = page.locator("#programStartBtn")
        expect(btn).to_be_visible()

    def test_review_form_has_three_textareas(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='review']").click()
        textareas = page.locator("#panel-review textarea")
        expect(textareas).to_have_count(3)

    def test_water_log_button_visible(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='productivity']").click()
        btn = page.locator("#logWaterBtn")
        expect(btn).to_be_visible()

    def test_planner_add_button_visible(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='productivity']").click()
        btn = page.locator("#plannerAddBtn")
        expect(btn).to_be_visible()

    def test_sr_add_card_button_visible(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='study']").click()
        btn = page.locator("#srAddBtn")
        expect(btn).to_be_visible()

    def test_reward_check_button_visible(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='rewards']").click()
        btn = page.locator("#rewardCheckBtn")
        expect(btn).to_be_visible()

    def test_chat_search_button_visible(self, page: Page):
        page.goto(f"{BASE}/dashboard.html")
        page.locator(".dash-tab[data-panel='chat']").click()
        btn = page.locator("#chatSearchBtn")
        expect(btn).to_be_visible()

    def test_auth_gate_shows_when_not_logged_in(self, page: Page):
        # Clear localStorage to simulate logged-out state
        page.goto(f"{BASE}/dashboard.html")
        page.evaluate("localStorage.removeItem('anaida_user_email')")
        page.reload()
        auth_gate = page.locator("#overviewAuth")
        expect(auth_gate).to_be_visible()
