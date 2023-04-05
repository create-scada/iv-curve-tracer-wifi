from microdot import Microdot
from microdot import send_file, redirect
import time
import json
import os

def create_webapp(iv_curve_tracer):
    
    app = Microdot()

    @app.route('/static/<path:path>')
    def static(request, path):
        return send_file('static/' + path)

    @app.after_request
    def cors(request, response):
        response.headers["Access-Control-Allow-Origin"]  = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        return response

    @app.get('/')
    def index(request):
        return redirect('/static/index.html')

    @app.route('/list')
    def list(request):
        results = []
        for filename in os.listdir('/data'):
            results.append(filename)
        return sorted(results, key=int, reverse=True)

    @app.route('/clear')
    def clear(request):
        for filename in os.listdir('/data'):
            os.remove(f'/data/{filename}')
        return 'OK'

    @app.route('/trace')
    def trace(request):
        filename = request.args['file']
        return send_file('/data/' + filename)
                

    @app.route('/run')
    def run(request):
        
        results = iv_curve_tracer.run()

        with open('num.txt') as f:
            num = f.read()
            num = num.strip()
            num = int(num)
            num += 1

        try:

            with open('num.txt', 'w') as f:
                f.write(str(num))

            with open(f'/data/{num}', 'w') as fp:

                fp.write('Voltage, Current\n')

                for (voltage, current) in results:
                    line = f'{voltage},{current}\n'
                    fp.write(line)

                fp.flush()
        except Exception as e:

            print(e)
            time.sleep(3)

        else:
            time.sleep(3)

        print('FINISHED')

        return 'Complete'

    return app
