// 提交按钮点击事件
$('#submit-button').on('click', function () {
    const input1 = $('#input1').val();
    const input2 = $('#input2').val();

    // 校验输入框是否为空
    if (!input1 || !input2) {
        alert('请填写所有字段');
        return;
    }

    let id = Date.now();
    // 插入到json中
    set_project_data(id, input1, input2);

    // 插入新行到表格
    const newRow = `
            <tr id="${id}">
                <td>${input1}</td>
                <td>${input2}</td>
                <td><button class="btn btn-danger btn-sm delete-button">删除</button></td>
            </tr>
        `;
    $('#projects-table').append(newRow);

    // 清空输入框
    $('#input1').val('');
    $('#input2').val('');

    alert('添加成功！');
});

// 删除按钮点击事件
$(document).on('click', '.delete-button', function () {
    let tr = $(this).closest('tr');
    let id = tr.attr("id");

    pywebview.api.get_project_data().then(function (project_data) {
        let new_data = deleteProjectById(project_data.projects, id)

        let project_new_data = {
            "projects": new_data
        }

        pywebview.api.set_project_data(project_new_data).then(function () {
            tr.remove();
            console.log("删除成功", project_new_data)
            alert('删除成功！');
        })

    })

});


function set_project_data(id, website, keywords) {
    let data = {
        "id": id,
        "website": website,
        "keywords": splitAndTrimString(keywords, ",")
    }

    pywebview.api.get_project_data().then(function (project_data) {
        project_data.projects.push(data)

        pywebview.api.set_project_data(project_data).then(function () {
            console.log("添加成功", project_data)
        })
    })

}

function splitAndTrimString(input, separator) {
    // 去除首位空格并将中间的多个空格替换为单个空格
    const trimmedInput = input.trim().replace(/\s+/g, ' ');

    // 按照指定的分隔符切分字符串并去除每个元素的空格
    const resultArray = trimmedInput.split(separator).map(item => item.trim());

    return resultArray;
}


function deleteProjectById(projects, idToDelete) {
    console.log(projects)
    return projects.filter(project => project.id !== Number(idToDelete));
}