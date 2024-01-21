
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "scrapeData") {
      // Assuming you have a backend server URL where the Python crawler is hosted
      var backendUrl = "http://127.0.0.1:5000/crawl"; 
      // Send a POST request to the backend server
      fetch(backendUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: request.url }),
      })
      .then(response => {
        console.log("響應狀態:", response.status);
        return response.json();
      })
      .then(data => {
        console.log("收到的數據:", data);
        // 將爬取的數據發送回 popup.js
        sendResponse({ success: true, data: data });
      })
      .catch(error => {
        console.error("錯誤:", error);     
        sendResponse({ success: false, error: error.message });
    });  
      // Return true to indicate that the response will be sent asynchronously
      return true;
    }
  });
  

