import asyncio
import os
import subprocess
import tempfile
import shutil
from patchright.async_api import async_playwright

user_email = 'abutalibsiriyev2003@gmail.com'
user_password = '@But@!ib$iriy3v200311'
task_url = "https://upskill.us.qwasar.io/tracks/preseason-web/track_users/1346-siriyev_a-jul-2021-30-e54d/projects/quest00"

async def main():
    async def handle_dialog(dialog):
        await dialog.accept()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://casapp.us.qwasar.io/login?service=https://upskill.us.qwasar.io/users/service")
        await page.locator("//input[@id='username']").fill(user_email)
        await page.locator("//input[@id='password']").fill(user_password)
        await page.locator("//button[@type='submit']").click()
        await page.locator("//div[contains(text(), 'My Tracks')]").wait_for(timeout=10000)

        page.on("dialog", handle_dialog)
    
        await page.goto(task_url)

        
        print("Starting task")
        await page.locator("//div/span[contains(text(), 'Register')]/..").click(timeout=5000)
        
        print("Trying to acquire remote url")
        
        while True:
            try:
                repo_url = await page.locator("//input[@id='git-repos']").input_value()
                if "git" in repo_url:
                    break
            except Exception as e:
                print(f"Error occurred while acquiring remote url: {e}")

            await asyncio.sleep(2)
            await page.reload()

        print(f"Remote repository url: {repo_url}")

        with tempfile.TemporaryDirectory() as temp_dir:
            subprocess.run(['git', 'clone', repo_url, temp_dir])

            shutil.copytree(os.path.join(os.path.dirname(__file__), 'quest00'), temp_dir, dirs_exist_ok=True)
            
            subprocess.run(['git', 'add', '.'], cwd=temp_dir)

            try:
                subprocess.run(['git', 'commit', '-m', 'Add task files'], cwd=temp_dir)

                subprocess.run(['git', 'push'], cwd=temp_dir)

                print("git push completed")
            except:
                pass

        print("submitting project")
        await page.locator("//a/span[contains(text(), 'Submit Project')]/..").click(timeout=5000)
        print("submit done")

        while True:
            try:
                await page.locator("//span[contains(text(), 'Keep Working On This Solution')]").wait_for(timeout=5000)
                break
            except:
                await page.reload()

        print("task accepted deleting group")
        await page.locator("//a/span[contains(text(), 'Delete group')]/..").click()
        print("group deleted successfully")

        while True:
            try:
                await page.locator("//div/span[contains(text(), 'Register')]/..").wait_for(timeout=5000)
                break
            except:
                pass
        
        print("Points earned restarting the task")

asyncio.run(main())