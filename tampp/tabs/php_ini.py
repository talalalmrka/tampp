from __future__ import annotations

import asyncio

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, LoadingIndicator, TabPane

from tampp.utils import php_ini_all
from tampp.widgets import ListGroup, ListGroupItem


class PhpIniTab(TabPane):
    def __init__(self, **kwargs):
        kwargs.setdefault("id", "php-ini-tab")
        title = kwargs.pop("title", "Php Ini")

        super().__init__(title, **kwargs)

        self.items = php_ini_all()

        # Build search index once.
        self.search_index = [
            (key, value, f"{key} {value}".lower()) for key, value in self.items.items()
        ]

        self.search_timer = None
        self.search_token = 0

    def compose(self) -> ComposeResult:
        yield Input(
            placeholder="Search PHP configuration...",
            id="php-ini-search",
        )

        yield LoadingIndicator(id="php-ini-loading")

        with VerticalScroll(id="php-ini-scroll"):
            yield ListGroup(
                items=[
                    ListGroupItem(
                        title=key,
                        subtitle=str(value),
                    )
                    for key, value in self.items.items()
                ],
                id="php-ini-list",
            )

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id != "php-ini-search":
            return

        query = event.value.strip().lower()

        self.search_token += 1

        if self.search_timer:
            self.search_timer.stop()

        loading = self.query_one("#php-ini-loading")
        loading.display = True

        self.search_timer = self.set_timer(
            0.3,
            lambda: self.start_search(query, self.search_token),
        )

    def start_search(self, query: str, token: int) -> None:
        self.run_worker(
            self.search(query, token),
            group="php-ini-search",
            exclusive=True,
        )

    def filter_items(self, query: str) -> list:
        if not query:
            return [(key, value) for key, value, _ in self.search_index]

        return [
            (key, value)
            for key, value, searchable in self.search_index
            if query in searchable
        ]

    async def search(self, query: str, token: int) -> None:
        try:
            loop = asyncio.get_running_loop()

            filtered = await loop.run_in_executor(
                None,
                self.filter_items,
                query,
            )

            # Ignore outdated search results.
            if token != self.search_token:
                return

            group = self.query_one("#php-ini-list", ListGroup)

            await group.remove_children()

            if filtered:
                await group.mount(
                    *[
                        ListGroupItem(
                            title=key,
                            subtitle=str(value),
                        )
                        for key, value in filtered
                    ]
                )

        finally:
            if token == self.search_token:
                self.query_one("#php-ini-loading").display = False
