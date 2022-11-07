#https://github.com/alethcoe/playwright_recording_pytest/blob/main/conftest.py
from fixtures.constants import *
import asyncio
from asyncio import AbstractEventLoop
from typing import Any, Callable, Dict, Generator, List, Optional
import os
import pytest
import variables

from playwright.sync_api import ( 
    Browser,
    BrowserContext,
    Page, APIRequestContext, Playwright

)

import os
import shutil

# @pytest.fixture(scope="session")
# def api_request_context(
#     playwright: Playwright,
# ) -> Generator[APIRequestContext, None, None]:
   
#     request_context = playwright.request.new_context()
#     yield request_context
#     request_context.dispose()


# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args, video_path):
#     if OVERRIDE_TEST_BROWSER_SIZE == True :
#         return {
#             **browser_context_args,
#             "record_video_dir": video_path,
#             "viewport": {
#                 "width": OVERRIDE_TEST_BROWSER_WIDTH,
#                 "height": OVERRIDE_TEST_BROWSER_HEIGHT
#                 }
#             }
#     if OVERRIDE_TEST_BROWSER_SIZE == False :
#         return {
#             **browser_context_args,
#             "record_video_dir": video_path,
#             "viewport": {
#                 "width": 1920,
#                 "height": 1080
#                 }
#             }

# @pytest.fixture(scope="session")
# def video_path():
#     return "./videos"

# @pytest.fixture(scope="session")
# def trace_path():
#     return "./traces"

# def pytest_sessionstart(session):
#     """
#     Called before test run starts
#     """
    
#     if os.path.exists("./videos"):
#         for filename in os.listdir("./videos"):
#             filepath = os.path.join("./videos", filename)
#             try:
#                 shutil.rmtree(filepath)
#             except OSError:
#                 os.remove(filepath)

# @pytest.fixture
# def page(context: BrowserContext, base_url: str) -> Generator[Page, None, None]:
#     context.set_default_timeout(2000000)
#     page = context.new_page()
#     page._goto = page.goto  # type: ignore
#     page.goto = lambda *args, **kwargs: _handle_page_goto(  # type: ignore
#         page, list(args), kwargs, base_url
#     )
#     yield page

#     #save off the test unique id
#     current_path_name = os.path.split(context.pages[0].video.path())[1]
#     BrowserContext.current_video_name = current_path_name

#     page.close()

# @pytest.fixture
# def context(
#     browser: Browser, browser_context_args: Dict, browser_name, video_path, trace_path, request
# ) -> Generator[BrowserContext, None, None]:
#     context = browser.new_context(**browser_context_args)
#     context.tracing.start(screenshots=True, snapshots=True)
#     current_failed_tests = request.session.testsfailed
#     yield context
#     current_video_name = context.current_video_name
#     current_video_path = os.path.join(video_path, current_video_name)
#     updated_video_path = os.path.join(video_path, f'{request.node.originalname}_{browser_name}.webm')

#     updated_trace_path = os.path.join(trace_path, f'{request.node.originalname}_{browser_name}.zip')
#     context.tracing.stop(path = updated_trace_path)
#     context.close()
#     os.rename(current_video_path, updated_video_path)
#     if request.session.testsfailed == current_failed_tests:
#         #test should have been successful no real reason to keep it
#         os.remove(updated_trace_path)
#         os.remove(updated_video_path)

# def _handle_page_goto(
#     page: Page, args: List[Any], kwargs: Dict[str, Any], base_url: str
# ) -> None:
#     url = args.pop()
#     if not (url.startswith("http://") or url.startswith("https://")):
#         url = base_url + url
#     return page._goto(url, *args, **kwargs)  # type: ignore
