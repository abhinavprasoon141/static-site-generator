# Architechture

The flow of data through the full system is:

-  Markdown files are in the /content directory. A template.html file is in the root of the project.
-  The static site generator (the Python code in src/) reads the Markdown files and the template file.
-  The generator converts the Markdown files to a final HTML file for each page and writes them to the /public directory.
-  We start the built-in Python HTTP server (a separate program, unrelated to the generator) to serve the contents of the /public directory on http://localhost:8888 (our local machine).
-  We open a browser and navigate to http://localhost:8888 to view the rendered site.

## How the SSG Works

The vast majority of our coding will happen in the src/ directory because almost all of the work is done in steps 2 and 3 above. Here's a rough outline of what the final program will do when it runs:

1. Delete everything in the /public directory.
2. Copy any static assets (HTML template, images, CSS, etc.) to the /public directory.
3. Generate an HTML file for each Markdown file in the /content directory. For each Markdown file:
      1. Open the file and read its contents.
      2. Split the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.).
      3. Convert each block into a tree of HTMLNode objects. For inline elements (like bold text, links, etc.) we will convert:
            Raw markdown -> TextNode -> HTMLNode
      4.  Join all the HTMLNode blocks under one large parent HTMLNode for the pages.
      5.  Use a recursive to_html() method to convert the HTMLNode and all its nested nodes to a giant HTML string and inject it in the HTML template.
      6.  Write the full HTML string to a file for that page in the /public directory.

![8f6de62ce2eb5d3275106cc9b14466c9.png](:/8dc0f5a067d14ebdb82dc0c8fca892ac)

