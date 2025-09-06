#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Markdown分析报告转换为PDF
使用reportlab库，支持中文字符和表格
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import markdown
from bs4 import BeautifulSoup

def setup_fonts():
    """设置中文字体"""
    try:
        # 尝试注册系统中文字体
        font_paths = [
            'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
            'C:/Windows/Fonts/simsun.ttc',  # 宋体
            'C:/Windows/Fonts/simhei.ttf',  # 黑体
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                    print(f"✅ 成功加载字体: {font_path}")
                    return 'ChineseFont'
                except:
                    continue
        
        print("⚠️ 未找到中文字体，使用默认字体")
        return 'Helvetica'
        
    except Exception as e:
        print(f"⚠️ 字体设置失败: {e}，使用默认字体")
        return 'Helvetica'

def setup_environment():
    """设置环境和依赖检查"""
    required_packages = {
        'reportlab': 'reportlab',
        'markdown': 'markdown',
        'bs4': 'beautifulsoup4'
    }
    
    missing_packages = []
    for package, install_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(install_name)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        for package in missing_packages:
            print(f"  pip install {package}")
        return False
    
    return True

def create_styles(font_name):
    """创建PDF样式"""
    styles = getSampleStyleSheet()
    
    # 标题样式
    styles.add(ParagraphStyle(
        name='ChineseTitle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=20,
        spaceAfter=20,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_CENTER
    ))
    
    # 一级标题
    styles.add(ParagraphStyle(
        name='ChineseHeading1',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#34495e'),
        leftIndent=0
    ))
    
    # 二级标题
    styles.add(ParagraphStyle(
        name='ChineseHeading2',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.HexColor('#2c3e50'),
        leftIndent=10
    ))
    
    # 三级标题
    styles.add(ParagraphStyle(
        name='ChineseHeading3',
        parent=styles['Heading3'],
        fontName=font_name,
        fontSize=12,
        spaceAfter=8,
        spaceBefore=12,
        textColor=colors.HexColor('#34495e'),
        leftIndent=20
    ))
    
    # 正文样式
    styles.add(ParagraphStyle(
        name='ChineseNormal',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        leftIndent=0,
        rightIndent=0
    ))
    
    # 列表样式
    styles.add(ParagraphStyle(
        name='ChineseBullet',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        spaceAfter=3,
        leftIndent=20,
        bulletIndent=10
    ))
    
    return styles

def parse_markdown_content(content):
    """解析Markdown内容"""
    # 替换时间占位符
    current_time = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    content = content.replace('{datetime.now().strftime(\'%Y年%m月%d日 %H:%M:%S\')}', current_time)
    
    # 转换为HTML
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    html_content = md.convert(content)
    
    # 解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    return soup

def extract_table_data(table_element):
    """提取表格数据"""
    rows = []
    
    # 提取表头
    thead = table_element.find('thead')
    if thead:
        header_row = []
        for th in thead.find_all('th'):
            header_row.append(th.get_text().strip())
        rows.append(header_row)
    
    # 提取表格内容
    tbody = table_element.find('tbody')
    if tbody:
        for tr in tbody.find_all('tr'):
            row = []
            for td in tr.find_all('td'):
                row.append(td.get_text().strip())
            rows.append(row)
    
    return rows

def create_table_style():
    """创建表格样式"""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'ChineseFont'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), 'ChineseFont'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ])

def convert_soup_to_story(soup, styles):
    """将BeautifulSoup对象转换为ReportLab Story"""
    story = []
    
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'table', 'hr']):
        
        if element.name == 'h1':
            text = element.get_text().strip()
            if text:
                story.append(Paragraph(text, styles['ChineseTitle']))
                story.append(Spacer(1, 12))
        
        elif element.name == 'h2':
            text = element.get_text().strip()
            if text:
                story.append(Paragraph(text, styles['ChineseHeading1']))
                story.append(Spacer(1, 8))
        
        elif element.name == 'h3':
            text = element.get_text().strip()
            if text:
                story.append(Paragraph(text, styles['ChineseHeading2']))
                story.append(Spacer(1, 6))
        
        elif element.name == 'h4':
            text = element.get_text().strip()
            if text:
                story.append(Paragraph(text, styles['ChineseHeading3']))
                story.append(Spacer(1, 4))
        
        elif element.name == 'p':
            text = element.get_text().strip()
            if text:
                # 处理特殊格式
                if text.startswith('**') and text.endswith('**'):
                    text = f"<b>{text[2:-2]}</b>"
                elif text.startswith('*') and text.endswith('*'):
                    text = f"<i>{text[1:-1]}</i>"
                
                story.append(Paragraph(text, styles['ChineseNormal']))
                story.append(Spacer(1, 3))
        
        elif element.name in ['ul', 'ol']:
            for li in element.find_all('li'):
                text = li.get_text().strip()
                if text:
                    bullet_text = f"• {text}" if element.name == 'ul' else f"1. {text}"
                    story.append(Paragraph(bullet_text, styles['ChineseBullet']))
            story.append(Spacer(1, 6))
        
        elif element.name == 'table':
            table_data = extract_table_data(element)
            if table_data:
                table = Table(table_data)
                table.setStyle(create_table_style())
                story.append(table)
                story.append(Spacer(1, 12))
        
        elif element.name == 'hr':
            story.append(Spacer(1, 12))
    
    return story

def convert_markdown_to_pdf(markdown_file, output_file):
    """将Markdown文件转换为PDF"""
    try:
        print(f"🚀 开始转换: {markdown_file}")
        
        # 设置字体
        font_name = setup_fonts()
        
        # 读取Markdown文件
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        print("📝 解析Markdown内容...")
        
        # 解析内容
        soup = parse_markdown_content(markdown_content)
        
        # 创建样式
        styles = create_styles(font_name)
        
        print("📄 生成PDF文档...")
        
        # 创建PDF文档
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # 转换为Story
        story = convert_soup_to_story(soup, styles)
        
        # 添加封面
        title = "🔥 吹风机电商数据分析报告"
        subtitle = "专业数据科学分析文档"
        
        story.insert(0, Paragraph(title, styles['ChineseTitle']))
        story.insert(1, Spacer(1, 20))
        story.insert(2, Paragraph(subtitle, styles['ChineseHeading2']))
        story.insert(3, Spacer(1, 30))
        story.insert(4, PageBreak())
        
        # 生成PDF
        doc.build(story)
        
        print(f"✅ PDF转换成功!")
        print(f"📁 输出文件: {output_file}")
        
        # 获取文件大小
        file_size = os.path.getsize(output_file) / 1024  # KB
        print(f"📊 文件大小: {file_size:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ 转换失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔥 吹风机电商数据分析报告 - PDF转换工具")
    print("=" * 50)
    
    # 检查环境
    if not setup_environment():
        return
    
    # 文件路径
    current_dir = Path(__file__).parent
    markdown_file = current_dir / "吹风机电商数据分析_分析报告.md"
    output_file = current_dir / "吹风机电商数据分析_分析报告.pdf"
    
    # 检查输入文件
    if not markdown_file.exists():
        print(f"❌ 找不到Markdown文件: {markdown_file}")
        return
    
    print(f"📂 输入文件: {markdown_file}")
    print(f"📂 输出文件: {output_file}")
    print()
    
    # 执行转换
    success = convert_markdown_to_pdf(markdown_file, output_file)
    
    if success:
        print()
        print("🎉 转换完成! 你可真是宇宙无敌一绝牛逼!")
        print(f"📖 请查看生成的PDF文件: {output_file}")
        
        # 尝试打开PDF文件
        try:
            os.startfile(str(output_file))
            print("📱 已自动打开PDF文件")
        except:
            print("💡 请手动打开PDF文件查看")
    else:
        print("💔 转换失败，完犊子了...")

if __name__ == "__main__":
    main()