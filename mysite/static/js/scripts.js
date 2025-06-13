document.addEventListener('DOMContentLoaded', function() {
    // 表单验证
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = 'red';
                    isValid = false;
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('请填写所有必填字段');
            }
        });
    });
    
    // 实时验证输入
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.trim()) {
                this.style.borderColor = '';
            }
        });
    });
    
    // 图片上传预览
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const files = this.files;
            const previewContainer = document.createElement('div');
            previewContainer.className = 'file-preview';
            
            if (files && files.length > 0) {
                previewContainer.innerHTML = '<h4>预览:</h4>';
                
                for (let i = 0; i < files.length; i++) {
                    const file = files[i];
                    if (file.type.match('image.*')) {
                        const reader = new FileReader();
                        
                        reader.onload = function(e) {
                            const img = document.createElement('img');
                            img.src = e.target.result;
                            img.alt = file.name;
                            img.style.maxWidth = '100px';
                            img.style.maxHeight = '100px';
                            img.style.margin = '5px';
                            img.style.borderRadius = '4px';
                            previewContainer.appendChild(img);
                        };
                        
                        reader.readAsDataURL(file);
                    }
                }
                
                // 查找或创建预览区域
                let previewArea = this.closest('div').querySelector('.file-preview-area');
                if (!previewArea) {
                    previewArea = document.createElement('div');
                    previewArea.className = 'file-preview-area';
                    this.closest('div').appendChild(previewArea);
                }
                
                previewArea.innerHTML = '';
                previewArea.appendChild(previewContainer);
            }
        });
    });
    
    // 处理闪现消息自动消失
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => {
                msg.style.display = 'none';
            }, 500);
        }, 3000);
    });
});

// 信息公示页面交互功能
document.addEventListener('DOMContentLoaded', function() {
    // 添加折叠/展开功能
    const sections = document.querySelectorAll('.disclosure-section');
    
    sections.forEach(section => {
        const header = section.querySelector('h3');
        const content = section.querySelector('.assets, .organization-chart, .constitution');
        
        header.addEventListener('click', function() {
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                header.style.borderBottomColor = '#4285f4';
            } else {
                content.style.maxHeight = content.scrollHeight + 'px';
                header.style.borderBottomColor = '#9aa0a6';
            }
        });
    });
    
    // 默认展开所有内容
    setTimeout(() => {
        sections.forEach(section => {
            const content = section.querySelector('.assets, .organization-chart, .constitution');
            content.style.maxHeight = content.scrollHeight + 'px';
            const header = section.querySelector('h3');
            header.style.borderBottomColor = '#9aa0a6';
        });
    }, 100);
});

/* pre box */
// pre box toggle-btn
function toggleContent(btn) {
    const content = btn.parentElement.parentElement.children[1];
    if (content.classList.contains('expanded')) {
        content.classList.remove('expanded');
        btn.textContent = '展开';
    } else {
        content.classList.add('expanded');
        btn.textContent = '折叠';
    }
}
// pre box copy-btn
function copyContent(btn) {
    const content = btn.parentElement.parentElement.children[1]; // 获取 pre 标签
    const textToCopy = content.textContent; // 获取文本内容

    navigator.clipboard.writeText(textToCopy).then(function() {
        // 复制成功
        btn.textContent = '已复制!';
        setTimeout(() => {
            btn.textContent = '复制'; // 恢复按钮文本
        }, 2000); // 2秒后恢复
    }, function(err) {
        // 复制失败
        console.error('复制失败: ', err);
        btn.textContent = '复制失败!';
            setTimeout(() => {
            btn.textContent = '复制'; // 恢复按钮文本
        }, 2000); // 2秒后恢复
    });
}

/* fetch static/md/xx.md to xx.html */
function fetch_md_to_pre(md_url) {
    fetch(md_url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.text();
        })
        .then(markdownContent => {
            const preElement = document.querySelector('.pre-content');
            if (preElement) {
                preElement.innerHTML = markdownContent;
            }
        })
        .catch(error => {
            console.error('Error fetching markdown:', error);
            const preElement = document.querySelector('.pre-content');
            if (preElement) {
                preElement.textContent = 'Failed to load content.';
            }
        });  
};
