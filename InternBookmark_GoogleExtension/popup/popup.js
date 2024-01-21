
document.addEventListener('DOMContentLoaded', function() {

    checkAndLoadTableData();
    document.getElementById('addBookmark').addEventListener('click', function() {
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            var currentUrl = tabs[0].url;

            // fetch data from the backend
            fetchDataFromBackend(currentUrl, function(response) {
                console.log(response.success)
                if (response.success === true) {                    
                    addToTable(response.data);
                } else {
                    console.error("Scraping failed:", response.error);
                }
            });
        });
    });
});

function clearlocalstorage(){
    chrome.storage.local.set({ 'tableData': null }, function() {
        console.log('Local storage cleared');
    });
}
function fetchDataFromBackend(url, callback) {
    // Send a message to the background script to initiate the scraping process
    chrome.runtime.sendMessage({ action: "scrapeData", url: url }, function(response) {
        callback(response); 
    });
}

function addToTable(data) {
    try{
        var testerror = data.data['實習名稱'];

        var tableBody = document.getElementById('bookmarkTable').getElementsByTagName('tbody')[0];
        var newRow = tableBody.insertRow(-1);
        console.log("var newRow = tableBody.insertRow(-1)");
        var fieldOrder = ['實習名稱','公司名稱','薪水','地點','更多資訊','原始連結'];
    
        for (var i = 0; i < fieldOrder.length; i++) {
            var cell = newRow.insertCell(-1);
            var fieldName = fieldOrder[i];
            cell.textContent = data.data[fieldName];  
        }
        saveTableDataToStorage();
    }
    catch (error) {
        // 在這裡捕獲特定的錯誤類型
        if (error instanceof TypeError) {
            alert("此實習已經紀錄過囉！");
            return; // 添加 return，終止函數執行
        }
    }
}

function saveTableDataToStorage() {
    var tableData = getTableDataFromDOM();
    chrome.storage.local.set({ 'tableData': tableData }, function() {
        console.log('Table data saved to storage:', tableData);
    });
}
function getTableDataFromDOM() {
    var table = document.getElementById('bookmarkTable');
    var tableData = Array.from(table.querySelectorAll('td')).map(td => td.textContent);
    return tableData;
}



function checkAndLoadTableData() {
    chrome.storage.local.get('tableData', function(result) {
        var tableData = result.tableData;
        if (tableData !== undefined) {
            // 這裡您可以將表格數據應用到您的 HTML 中，這是一個示例
            applyTableDataToDOM(tableData);
            console.log("執行applyTableDataToDOM(tableData);");
        }
        else{
            console.log("第一次打開套件");
        }
    });
}
function applyTableDataToDOM(data) {
    var table = document.getElementById('bookmarkTable');
    var tbody = table.querySelector('tbody');
    var colCount = 6;
    var datarowcount = (data.length)/colCount;
    // 遍歷數據
    for (var i = 0; i < datarowcount; i++) {
        // 創建新的行
        var newRow = tbody.insertRow(-1);
        // 遍歷每一列
        for (var j = 0; j < colCount; j++) {
            // 創建新的單元格
            var cell = newRow.insertCell(-1);
            // 計算對應的數據索引
            var dataIndex = i * colCount + j;
            // 檢查數據索引是否超出數據陣列的範圍
            if (dataIndex < data.length) {
                // 將數據應用到對應的 <td> 元素
                cell.textContent = data[dataIndex];
            }
        }
    }
}









