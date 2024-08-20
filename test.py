import asyncio
from playwright.async_api import async_playwright

async def file_to_pdf(file_path, output_path):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            # Read the local HTML file
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            # Set the HTML content
            await page.set_content(html_content, wait_until='networkidle')
            
            # Generate PDF with options to fit content to a single page
            await page.pdf(
                path=output_path,
                format='A4',  # Or other formats like 'Letter'
                print_background=True,
                margin={'top': '10px', 'bottom': '10px', 'left': '10px', 'right': '10px'}
                # scale=0.8  # Adjust the scale to fit content
            )
            
            await browser.close()
            print(f"PDF successfully generated at {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file_path = 'D:/Softwares/Invoice-generator-html/tmpy7hm000f.html'
output_path = 'html-to-pdf-output.pdf'

asyncio.run(file_to_pdf(file_path, output_path))
