comment_view("first");
async function comment_view(times){
    const msgBoardView = document.querySelector(".msg-board-view");
    try{
        let response;
        if (times === "first"){
            response = await fetch(`/api/comment?times=${1}`, {
                method: "GET"
            });
        }else if(times === "second"){
             response = await fetch(`/api/comment?times=${2}`, {
                method: "GET"
            });
        }
        

        const dt = await response.json();

        if (!response.ok || dt.error !== undefined){
            console.log("取留言資料失敗。");
            return;
        }

        const result = dt.result;
        for (let i=0; i < result.length; i++){
            const viewCommentInfo = document.createElement("div");
            viewCommentInfo.classList.add("view-comment-info");
            // 留言
            const commentInfoText = document.createElement("div");
            commentInfoText.classList.add("comment-info-text");
            const infoText = document.createElement("div");
            infoText.classList.add("info-text");
            infoText.textContent = String(result[i]["comment"]);
            commentInfoText.appendChild(infoText);
            // 圖片顯示
            const commentInfoImage = document.createElement("div");
            commentInfoImage.classList.add("comment-info-image");
            const infoImage = document.createElement("img");
            infoImage.src = String(result[i]["image_name"]);
            commentInfoImage.appendChild(infoImage);

            viewCommentInfo.appendChild(commentInfoText);
            viewCommentInfo.appendChild(commentInfoImage);

            msgBoardView.appendChild(viewCommentInfo);
        }
    }catch{
        console.log("取留言資料失敗。");
    };
};

let files; 

const fileUpload = document.getElementById("image-upload");
fileUpload.addEventListener("change", (e) => {
    files = e.target.files[0];
});

async function submit_comment() {
    const commentObj = document.getElementById("comment-text-input");
    const commentStr = commentObj.value.trim();
    if (commentStr !== ""){
        if (files !== undefined){
            const formData = new FormData();
            formData.append("comment_text", commentStr);
            formData.append("image", files);
        
            try{
                const response = await fetch("/api/comment",{
                    method: "POST",
                    body:formData,
                });

                const dt = await response.json();

                if (!response.ok || dt.error !== undefined){
                    console.log("留言發生錯誤，請稍後再試。");
                    return;
                }else{
                    commentObj.value="";
                    fileUpload.value="";
                    comment_view("second");
                };

            }catch{
                console.log("留言發生錯誤。");
            }
        };
    }
}

const submitBtn = document.getElementById("submit-btn");
if (submitBtn){
    submitBtn.addEventListener("click", function() {
        submit_comment();
    });
}

