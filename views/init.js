// 确保 pywebview 已经存在
function checkPywebview() {
    if (window.pywebview) {
        clearInterval(intervalId);
        console.log('pywebview 加载成功')
        init()
    }
}

let intervalId = setInterval(checkPywebview, 100);


function init() {
    // 获取设置数据
    pywebview.api.get_setting().then(function (data) {
        console.log('数据！', data)
        $('#auto-start').val(data.isStart);
        $('#frequency').val(data.frequency);

        // 判断是否需要自动运行
        if (data.isStart === "True") {
            let button_element = $('#start-button')
            if (button_element.text() === "开始执行") {
                button_element.text("停止执行")
                button_element.removeClass('btn-success').addClass('btn-danger')
                pywebview.api.start().then(function () {

                })
            }
        }
    })

    // 获取项目数据
    pywebview.api.get_project_data().then(function (project_data) {
        console.log('数据！', project_data)

        project_data.projects.forEach((project) => {
            // 插入新行到表格
            const newRow = `
                <tr id="${project.id}">
                    <td>${project.website}</td>
                    <td>${project.keywords.join(",")}</td>
                    <td><button class="btn btn-danger btn-sm delete-button">删除</button></td>
                </tr>
            `;
            $('#projects-table').append(newRow);
        })

    })
}


