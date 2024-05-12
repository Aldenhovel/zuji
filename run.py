import json
import random

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import pathlib
sys.path.append(pathlib.Path('./src/').absolute().__str__())

from src import utils
from src import algorithm
from src.CustomData import YSZJData, LGZJData, KMLData
from src.StandardData import StandardData

app = Flask(__name__, template_folder='./templates/', static_folder='./static/')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/getDataSource', methods=["POST"])
def getDataSource():
    data = request.get_json()
    field = data['sourceField']
    data_source = utils.getAllDataSource(field)
    response = {
        'dataSource': data_source
    }
    return jsonify(response)

@app.route('/processPreview', methods=["POST"])
def processPreview():
    try:
        data = request.get_json()
        data_source = data['dataSource']
        merged_df = StandardData.mergeAllDataSource(data_source)
        clusters, ready_shortcut = StandardData.processToWebUI(merged_df, config['kMeansCluster'])
        #map_path = algorithm.reDrawPoints(merged_df, save_dir='static/tmp/')
        response = {
            'mapData': clusters,
            'readyShortcut': ready_shortcut,
            'pointCount': len(merged_df),
            #'mapPath': map_path
        }
        return jsonify(response)
    except Exception as e:
        print(e)


@app.route('/getConfigInfo', methods=["GET"])
def getConfigInfo():
    response = {
        'kMeansCluster': config['kMeansCluster'],
        'mapType': config['mapType']
    }
    return jsonify(response)


@app.route('/processShortcut', methods=["POST"])
def processShortcut():
    data = request.get_json()
    data_source = data['dataSource']
    merged_df = StandardData.mergeAllDataSource(data_source)
    filename = utils.genFileName()
    StandardData.save(merged_df, os.path.join('./data/shortcut', filename))
    response = {
        'status': True,
        'shortcutPath': filename,
    }
    return jsonify(response)

@app.route('/processExport', methods=["POST"])
def processExport():
    data = request.get_json()
    shortcut_source = data['shortcutSource'].split('】')[-1]
    export_type = data['exportType']
    as_name = data['asName']
    if as_name == '':
        as_name = utils.genFileName(_format='')
    df = StandardData.load(os.path.join('data/shortcut', shortcut_source))
    export_path = os.path.join('data/export', f'{as_name}-{export_type}.csv')
    if export_type == "yszj-ios":
        export_path = os.path.join('data/export', f'{as_name}-{export_type}.csv')
        df = StandardData.cvtToYSZJFormat(df)
        YSZJData.export(df, export_path)
        status = True
    elif export_type == "lgzj-android":
        export_path = os.path.join('data/export', f'{as_name}-{export_type}.csv')
        df = StandardData.cvtToLGZJFormat(df, export_os="android")
        LGZJData.export(df, export_path)
        status = True
    elif export_type == "lgzj-ios":
        export_path = os.path.join('data/export', f'{as_name}-{export_type}.csv')
        df = StandardData.cvtToLGZJFormat(df, export_os="ios")
        LGZJData.export(df, export_path)
        status = True
    elif export_type == "google-earth":
        export_path = os.path.join('data/export', f'{as_name}-{export_type}.kml')
        tree = StandardData.cvtToKMLFormat(df)
        KMLData.export(tree, export_path)
        status = True
    else:
        status = False
    response = {
        'status': status,
        'message': f'Export file as 【{export_path}】' if status else 'Failed.'
    }
    return jsonify(response)


@app.route('/removeShortcutFiles', methods=["GET"])
def removeShortcutFiles():
    file_count = utils.clearFolder('./data/shortcut/')
    response = {
        'status': f'Done, {file_count} files were removed.'
    }
    return jsonify(response)

@app.route('/removeExportFiles', methods=["GET"])
def removeExportFiles():
    file_count = utils.clearFolder('./data/export/')
    response = {
        'status': f'Done, {file_count} files were removed.'
    }
    return jsonify(response)

@app.route('/removeTmpFiles', methods=["GET"])
def removeTmpFiles():
    file_count = 0
    file_count += utils.clearFolder('./data/tmp/')
    file_count += utils.clearFolder('./static/tmp/')
    response = {
        'status': f'Done, {file_count} files were removed.'
    }
    return jsonify(response)

@app.route('/quickstart', methods=["POST"])
def quickstart():
    file = request.files['file']
    to_type = request.form['type']
    file.save('./data/tmp/upload_data.csv')
    if to_type == 'YSZJ2LGZJ':
        df = YSZJData.read('upload_data.csv', default_dir='./data/tmp')
        df = YSZJData.cvtToStandardFormat(df)
        df = StandardData.cvtToLGZJFormat(df)
        LGZJData.export(df, './data/tmp/res_data.csv')
    elif to_type == 'LGZJ2YSZJ':
        df = LGZJData.read('upload_data.csv', default_dir='./data/tmp')
        df = LGZJData.cvtToStandardFormat(df)
        df = StandardData.cvtToYSZJFormat(df)
        YSZJData.export(df, './data/tmp/res_data.csv')

    csv_data = './data/tmp/res_data.csv'
    return send_file(
        csv_data,
        mimetype='text/csv',
        as_attachment=True,
        download_name='downloaded_file.csv'
    )


if __name__ == "__main__":
    import sys
    sys.path.append('.')

    config = dict()
    with open('./config.json', 'r') as f:
        data = json.load(f)
        config['kMeansCluster'] = int(data['kMeansCluster'])
        config['mapType'] = data['mapType']
    app.run()


