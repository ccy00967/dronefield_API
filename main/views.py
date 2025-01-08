from django.http import HttpResponse

def home(request):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dronefild API</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>Dronefild_ API</h1>
        <p>환영합니다! Dronefild API에 오신 것을 환영합니다.</p>
    </body>
    </html>
    """
    return HttpResponse(html_content)