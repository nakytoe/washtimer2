
PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title> <!-- Replace with your page title -->
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
        .number {
            font-size: 72px; /* Large digital number */
            margin: 20px 0;
        }
        .description {
            margin: 20px 0;
            font-size: 18px;
        }
        a {
            color: blue;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>WashTimer</h1>

    <p class="description">
        Set timer for 3 hour program to begin in 
    </p>

    <div class="number">
        [begin_hours] h
    </div>

    <p class="description">
        or to end in
    </p>

    <div class="number">
        [end_hours] h
    </div>

    <p class="description">
        for the cheapest wash in the next 12 hours.
    </p>

    <p class="description">
        WashTimer by Nuutti Kytö 2024
    </p>

    <p class="description">
        <a href="https://github.com/nakytoe/washtimer2">source code in GitHub</a>
    </p>
</body>
</html>
"""

def get_page_html(begin_hours:int, end_hours:int)->str:
    return PAGE_HTML.replace("[begin_hours]", str(begin_hours)).replace("[end_hours]", str(end_hours))

