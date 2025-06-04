// Main JavaScript for Python SQLi-Labs
$(document).ready(function() {
    // 页面加载动画
    $('body').addClass('loaded');
    
    // 卡片悬停效果
    $('.lab-card, .card').hover(
        function() {
            $(this).addClass('shadow-lg').css('transform', 'translateY(-5px)');
        },
        function() {
            $(this).removeClass('shadow-lg').css('transform', 'translateY(0)');
        }
    );
    
    // 平滑滚动
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if (target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 80
            }, 1000);
        }
    });
    
    // 代码高亮点击复制
    $('.code-display, .bg-dark code').click(function() {
        var text = $(this).text();
        navigator.clipboard.writeText(text).then(function() {
            // 显示复制成功提示
            showToast('代码已复制到剪贴板', 'success');
        }).catch(function() {
            // 降级方案
            var range = document.createRange();
            range.selectNode(this);
            window.getSelection().removeAllRanges();
            window.getSelection().addRange(range);
            showToast('代码已选中，请手动复制', 'info');
        });
    });
    
    // 表单提交增强
    $('form').on('submit', function() {
        var submitBtn = $(this).find('button[type="submit"]');
        var originalText = submitBtn.html();
        
        // 显示加载状态
        submitBtn.html('<span class="loading"></span> 处理中...').prop('disabled', true);
        
        // 如果是GET请求且页面会刷新，恢复按钮状态
        setTimeout(function() {
            submitBtn.html(originalText).prop('disabled', false);
        }, 3000);
    });
    
    // 快速测试按钮增强
    $('.btn-outline-danger, .btn-outline-warning, .btn-outline-info, .btn-outline-success').click(function(e) {
        // 如果是测试按钮且有输入框，则填充数据而不是直接跳转
        if ($(this).attr('href') && $('input[name="id"]').length > 0) {
            e.preventDefault();
            var url = new URL(this.href, window.location.origin);
            var id = url.searchParams.get('id');
            if (id) {
                $('input[name="id"]').val(decodeURIComponent(id));
                $('form').submit();
            }
        }
    });
    
    // 警告消息自动隐藏
    $('.alert').each(function() {
        var alert = $(this);
        if (!alert.hasClass('alert-danger')) {
            setTimeout(function() {
                alert.fadeOut();
            }, 5000);
        }
    });
    
    // 表格行点击高亮
    $('table tbody tr').click(function() {
        $(this).toggleClass('table-active');
    });
    
    // 输入框焦点效果
    $('.form-control').focus(function() {
        $(this).parent().addClass('input-focus');
    }).blur(function() {
        $(this).parent().removeClass('input-focus');
    });
});

// 显示Toast消息
function showToast(message, type = 'info') {
    var toastHtml = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999;">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    $('body').append(toastHtml);
    var toast = new bootstrap.Toast($('.toast').last()[0]);
    toast.show();
    
    // 3秒后自动移除
    setTimeout(function() {
        $('.toast').last().remove();
    }, 3000);
}

// 错误处理
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
});

// 页面可见性API - 当用户切换标签页时暂停某些操作
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // 页面隐藏时的操作
        console.log('页面已隐藏');
    } else {
        // 页面显示时的操作
        console.log('页面已显示');
    }
});

// 检测暗黑模式偏好
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    // 用户偏好暗黑模式
    console.log('用户偏好暗黑模式');
}

// 响应式断点检测
function checkBreakpoint() {
    var width = $(window).width();
    if (width < 576) {
        $('body').addClass('mobile').removeClass('tablet desktop');
    } else if (width < 992) {
        $('body').addClass('tablet').removeClass('mobile desktop');
    } else {
        $('body').addClass('desktop').removeClass('mobile tablet');
    }
}

$(window).resize(checkBreakpoint);
checkBreakpoint(); // 初始检测 