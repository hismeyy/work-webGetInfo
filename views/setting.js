data = {
    "isStart": false,
    "frequency": 2
}

// 保存按钮点击事件
$('#save-button').on('click', function () {
    const isStart = $('#auto-start').val();
    const frequency = $('#frequency').val();

    data.isStart = isStart;
    data.frequency = frequency;

    console.log('是否开机自动启动:', isStart);
    console.log('爬取数据频率:', frequency);

    pywebview.api.set_setting(data).then(function () {
        alert('保存成功！');
    })

});