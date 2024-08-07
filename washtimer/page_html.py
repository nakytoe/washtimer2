
PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>WashTimer</title> <!-- Updated page title -->
 <style>
 body {
   font-family: 'Roboto', Arial, sans-serif;
   background-color: #f5f5f5;
   color: #333;
   text-align: center;
   padding: 40px;
   margin: 0;
 }
 h1 {
   font-size: 48px;
   color: #2c3e50;
 }
 p.description {
   margin: 10px 0;
   font-size: 20px;
 }
 .number {
   font-size: 72px; /* Large digital number */
   margin: 20px 0;
   color: #27ae60;
   display: flex;
   justify-content: center;
   align-items: center;
 }
 .number span {
   margin: 0 10px;
 }
 a {
   color: #2980b9;
   text-decoration: none;
 }
 a:hover {
   text-decoration: underline;
 }
 footer {
   margin-top: 40px;
   font-size: 14px;
 }
 </style>
 <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
 <h1>WashTimer</h1>
 <p class="description">Set your 3-hour program to start in</p>
 <div class="number">
   [begin_hours] h
 </div>
 <p class="description">or to finish in</p>
 <div class="number">
   [end_hours] h
 </div>
 <p class="description">for the cheapest wash in the next 12 hours.</p>
 <footer>
   <p>WashTimer by Nuutti Kytö, 2024</p>
   <p><a href="https://github.com/nakytoe/washtimer2">Source Code on GitHub</a></p>
 </footer>
</body>
</html>
"""

def get_page_html(begin_hours:int, end_hours:int)->str:
    return PAGE_HTML.replace("[begin_hours]", str(begin_hours)).replace("[end_hours]", str(end_hours))

