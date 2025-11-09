#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Markdown 转换 Web 服务 - 简化版
HTML 导出可通过浏览器打印为 PDF
"""

from flask import Flask, request, send_file, render_template_string
from werkzeug.utils import secure_filename
from converter import MarkdownConverter

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Web 界面 HTML
HTML_UI = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown 转换工具</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 1.1em; }
        .content { padding: 40px; }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 12px;
            padding: 60px 40px;
            text-align: center;
            background: linear-gradient(135deg, #f8f9ff 0%, #e8e9ff 100%);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .upload-area:hover {
            border-color: #764ba2;
            transform: scale(1.02);
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
        }
        .upload-area.dragover {
            background: linear-gradient(135deg, #e8e9ff 0%, #d8d9ff 100%);
            border-color: #764ba2;
        }
        .upload-icon { font-size: 72px; margin-bottom: 20px; animation: float 3s ease-in-out infinite; }
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        .upload-text {
            font-size: 1.4em;
            color: #667eea;
            margin-bottom: 10px;
            font-weight: 600;
        }
        .upload-hint { color: #6c757d; font-size: 0.95em; }
        #fileInput { display: none; }
        .file-info {
            margin-top: 25px;
            padding: 20px;
            background: linear-gradient(135deg, #e7f3ff 0%, #d7e9ff 100%);
            border-radius: 8px;
            border-left: 4px solid #667eea;
            display: none;
        }
        .file-info.show { display: block; animation: slideIn 0.3s ease; }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .file-info strong { color: #667eea; }
        .export-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 18px 25px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }
        .btn:active { transform: translateY(-1px); }
        .btn:disabled {
            background: linear-gradient(135deg, #ccc 0%, #999 100%);
            cursor: not-allowed;
            transform: none;
        }
        .btn-icon { font-size: 1.3em; }
        .status {
            margin-top: 20px;
            padding: 18px;
            border-radius: 8px;
            display: none;
            font-weight: 500;
        }
        .status.show { display: block; animation: slideIn 0.3s ease; }
        .status.success {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            color: #155724;
            border-left: 4px solid #28a745;
        }
        .status.error {
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            color: #721c24;
            border-left: 4px solid #dc3545;
        }
        .status.info {
            background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
            color: #0c5460;
            border-left: 4px solid #17a2b8;
        }
        .tip {
            margin-top: 30px;
            padding: 20px;
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            border-radius: 8px;
            color: #856404;
        }
        .tip strong { color: #856404; }
        .features {
            margin-top: 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
        }
        .feature {
            text-align: center;
            padding: 25px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 12px;
            transition: transform 0.3s ease;
        }
        .feature:hover { transform: translateY(-5px); }
        .feature-icon { font-size: 52px; margin-bottom: 12px; }
        .feature-title {
            font-weight: 700;
            margin-bottom: 8px;
            color: #667eea;
            font-size: 1.1em;
        }
        .feature-desc { font-size: 0.9em; color: #6c757d; line-height: 1.5; }
        .progress {
            width: 100%;
            height: 4px;
            background: #e9ecef;
            border-radius: 2px;
            overflow: hidden;
            margin-top: 15px;
            display: none;
        }
        .progress.show { display: block; }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            animation: progress 1.5s ease-in-out infinite;
        }
        @keyframes progress {
            0% { width: 0%; }
            50% { width: 70%; }
            100% { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 Markdown 转换工具</h1>
            <p>支持转换为 HTML 和 Word (DOCX)</p>
        </div>
        
        <div class="content">
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📄</div>
                <div class="upload-text">点击或拖拽上传 Markdown 文件</div>
                <div class="upload-hint">支持 .md 和 .markdown 格式 (最大 16MB)</div>
                <input type="file" id="fileInput" accept=".md,.markdown">
            </div>
            
            <div class="file-info" id="fileInfo"></div>
            <div class="progress" id="progress"><div class="progress-bar"></div></div>
            
            <div class="export-buttons" id="exportButtons" style="display: none;">
                <button class="btn" onclick="convert('html')">
                    <span class="btn-icon">📥</span>
                    <span>转换为 HTML (可打印PDF)</span>
                </button>
                <button class="btn" onclick="convert('docx')">
                    <span class="btn-icon">📥</span>
                    <span>转换为 Word</span>
                </button>
            </div>
            
            <div class="status" id="status"></div>
            
            <div class="tip">
                <strong>💡 导出 PDF 的方法：</strong><br>
                1. 点击"转换为 HTML" 按钮下载 HTML 文件<br>
                2. 用浏览器打开 HTML 文件<br>
                3. 按 Ctrl+P 或点击页面右上角"打印/保存为PDF"按钮<br>
                4. 在打印对话框中选择"保存为 PDF"
            </div>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🎨</div>
                    <div class="feature-title">美观排版</div>
                    <div class="feature-desc">自动优化格式和样式，专业美观</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">表格支持</div>
                    <div class="feature-desc">完美转换 Markdown 表格</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">💻</div>
                    <div class="feature-title">代码高亮</div>
                    <div class="feature-desc">保留代码块格式和样式</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentFile = null;
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const exportButtons = document.getElementById('exportButtons');
        const status = document.getElementById('status');
        const progress = document.getElementById('progress');
        
        uploadArea.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => {
            if (e.target.files[0]) handleFile(e.target.files[0]);
        });
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
        });
        
        function handleFile(file) {
            if (!file.name.match(/\\.(md|markdown)$/i)) {
                showStatus('error', '❌ 请上传 .md 或 .markdown 格式的文件');
                return;
            }
            
            currentFile = file;
            fileInfo.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>📄 文件名：</strong>${file.name}<br>
                        <strong>📦 大小：</strong>${(file.size / 1024).toFixed(2)} KB
                    </div>
                    <div style="font-size: 2em;">✅</div>
                </div>
            `;
            fileInfo.classList.add('show');
            exportButtons.style.display = 'grid';
            showStatus('info', '✨ 文件已就绪，请选择导出格式');
        }
        
        async function convert(format) {
            if (!currentFile) return;
            
            const formatNames = { html: 'HTML', docx: 'Word' };
            showStatus('info', `⏳ 正在转换为 ${formatNames[format]}...`);
            progress.classList.add('show');
            
            const formData = new FormData();
            formData.append('file', currentFile);
            formData.append('format', format);
            
            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = currentFile.name.replace(/\\.(md|markdown)$/i, `.${format}`);
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                    
                    progress.classList.remove('show');
                    
                    if (format === 'html') {
                        showStatus('success', '✅ HTML 已下载！打开文件后按 Ctrl+P 即可保存为 PDF');
                    } else {
                        showStatus('success', `✅ ${formatNames[format]} 转换成功！文件已下载`);
                    }
                } else {
                    const error = await response.text();
                    progress.classList.remove('show');
                    showStatus('error', `❌ 转换失败: ${error}`);
                }
            } catch (error) {
                progress.classList.remove('show');
                showStatus('error', `❌ 转换失败: ${error.message}`);
            }
        }
        
        function showStatus(type, message) {
            status.className = 'status show ' + type;
            status.textContent = message;
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_UI)


@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return '未上传文件', 400
    
    file = request.files['file']
    format_type = request.form.get('format', 'html')
    
    if not file.filename or not file.filename.endswith(('.md', '.markdown')):
        return '不支持的文件格式', 400
    
    try:
        md_content = file.read().decode('utf-8')
        converter = MarkdownConverter()
        
        filename = secure_filename(file.filename.rsplit('.', 1)[0])
        
        if format_type == 'html':
            html_content = converter.to_html(md_content, title=filename)
            from io import BytesIO
            html_bytes = BytesIO(html_content.encode('utf-8'))
            return send_file(
                html_bytes,
                mimetype='text/html',
                as_attachment=True,
                download_name=f'{filename}.html'
            )
        
        elif format_type == 'docx':
            docx_bytes = converter.to_docx(md_content)
            return send_file(
                docx_bytes,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                as_attachment=True,
                download_name=f'{filename}.docx'
            )
        
        else:
            return '不支持的输出格式', 400
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f'转换失败: {str(e)}', 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🚀 Markdown 转换工具已启动")
    print("="*60)
    print("\n  📍 访问地址: http://localhost:5000")
    print("\n  💡 支持格式:")
    print("     - HTML (通过浏览器打印可转为 PDF)")
    print("     - Word (DOCX)")
    print("\n  💡 完整 Mermaid 图表支持请使用 index.html")
    print("\n  💡 按 Ctrl+C 停止服务\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
