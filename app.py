#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Markdown 转换 Web 服务
提供 Web 界面进行 Markdown 转换
"""

import os
import tempfile
from pathlib import Path
from flask import Flask, render_template_string, request, send_file, jsonify
from werkzeug.utils import secure_filename
from md2pdf import MarkdownConverter
from md2docx import MarkdownToDocx

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# HTML 模板
HTML_TEMPLATE = """
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
            max-width: 800px;
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
            border-radius: 8px;
            padding: 60px 40px;
            text-align: center;
            background: #f8f9ff;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .upload-area:hover { border-color: #764ba2; background: #e8e9ff; transform: scale(1.02); }
        .upload-icon { font-size: 64px; margin-bottom: 20px; }
        .upload-text { font-size: 1.3em; color: #667eea; margin-bottom: 10px; font-weight: 600; }
        .upload-hint { color: #6c757d; }
        #fileInput { display: none; }
        .file-info {
            margin-top: 20px;
            padding: 20px;
            background: #e7f3ff;
            border-radius: 8px;
            display: none;
        }
        .file-info.show { display: block; }
        .export-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 35px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6); }
        .btn:active { transform: translateY(0); }
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }
        .status.show { display: block; }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .status.info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .features {
            margin-top: 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .feature {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .feature-icon { font-size: 48px; margin-bottom: 10px; }
        .feature-title { font-weight: 600; margin-bottom: 5px; color: #667eea; }
        .feature-desc { font-size: 0.9em; color: #6c757d; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 Markdown 转换工具</h1>
            <p>支持转换为 PDF、Word (DOCX) 和 HTML</p>
        </div>
        
        <div class="content">
            <div class="upload-area" id="uploadArea">
                <div class="upload-icon">📄</div>
                <div class="upload-text">点击或拖拽上传 Markdown 文件</div>
                <div class="upload-hint">支持 .md 和 .markdown 格式，最大 16MB</div>
                <input type="file" id="fileInput" accept=".md,.markdown">
            </div>
            
            <div class="file-info" id="fileInfo"></div>
            
            <div class="export-buttons" id="exportButtons" style="display: none;">
                <button class="btn" onclick="convert('pdf')">📥 转换为 PDF</button>
                <button class="btn" onclick="convert('docx')">📥 转换为 Word</button>
                <button class="btn" onclick="convert('html')">📥 转换为 HTML</button>
            </div>
            
            <div class="status" id="status"></div>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🎨</div>
                    <div class="feature-title">美观排版</div>
                    <div class="feature-desc">自动优化格式和样式</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">表格支持</div>
                    <div class="feature-desc">完美转换 Markdown 表格</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">💻</div>
                    <div class="feature-title">代码高亮</div>
                    <div class="feature-desc">保留代码块格式</div>
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
        
        uploadArea.addEventListener('click', () => fileInput.click());
        
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) handleFile(file);
        });
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#764ba2';
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.borderColor = '#667eea';
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = '#667eea';
            const file = e.dataTransfer.files[0];
            if (file) handleFile(file);
        });
        
        function handleFile(file) {
            if (!file.name.match(/\\.(md|markdown)$/i)) {
                showStatus('error', '请上传 .md 或 .markdown 格式的文件');
                return;
            }
            
            currentFile = file;
            fileInfo.innerHTML = `
                <strong>文件名：</strong>${file.name}<br>
                <strong>大小：</strong>${(file.size / 1024).toFixed(2)} KB
            `;
            fileInfo.classList.add('show');
            exportButtons.style.display = 'flex';
            showStatus('info', '文件已上传，请选择导出格式');
        }
        
        async function convert(format) {
            if (!currentFile) return;
            
            showStatus('info', `正在转换为 ${format.toUpperCase()}...`);
            
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
                    
                    showStatus('success', `✅ ${format.toUpperCase()} 转换成功！`);
                } else {
                    const error = await response.text();
                    showStatus('error', `转换失败: ${error}`);
                }
            } catch (error) {
                showStatus('error', `转换失败: ${error.message}`);
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
    """主页"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/convert', methods=['POST'])
def convert():
    """转换文件"""
    if 'file' not in request.files:
        return '未上传文件', 400
    
    file = request.files['file']
    format_type = request.form.get('format', 'pdf')
    
    if file.filename == '':
        return '未选择文件', 400
    
    if not file.filename.endswith(('.md', '.markdown')):
        return '不支持的文件格式', 400
    
    try:
        # 读取文件内容
        md_content = file.read().decode('utf-8')
        
        # 生成输出文件名
        base_name = secure_filename(file.filename.rsplit('.', 1)[0])
        output_filename = f"{base_name}.{format_type}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # 转换
        if format_type == 'pdf':
            converter = MarkdownConverter()
            converter.to_pdf(md_content, output_path)
        elif format_type == 'docx':
            converter = MarkdownToDocx()
            converter.convert(md_content, output_path)
        elif format_type == 'html':
            converter = MarkdownConverter()
            converter.to_html(md_content, output_path)
        else:
            return '不支持的输出格式', 400
        
        # 发送文件
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename
        )
    
    except Exception as e:
        return f'转换失败: {str(e)}', 500
    finally:
        # 清理临时文件
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass


if __name__ == '__main__':
    print("=" * 50)
    print("  Markdown 转换 Web 服务")
    print("=" * 50)
    print("\n访问地址: http://localhost:5000")
    print("\n按 Ctrl+C 停止服务\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

