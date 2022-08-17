// When the button is clicked, inject setPageBackgroundColor into current page
changeColor.addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({active: true, currentWindow: true});

    chrome.scripting.executeScript({
        target: {tabId: tab.id},
        function: setPageBackgroundColor,
    });
});


// The body of this function will be executed as a content script inside the
// current page
function setPageBackgroundColor() {
    main()


    function main() {
        let index = 0;
        let currArticle = null;

        const id = setInterval(() => {
            getNextArticle(currArticle).then((nextArticle) => {
                // 找到了
                index = index + 1
                currArticle = nextArticle
                console.log('find new one ' + index)
                // 删除判断
                const needDelete = judgeDelete(currArticle);
                console.log('need delete: ' + needDelete)
                if (needDelete) {
                    deleteThis(currArticle)
                }
            }).catch(() => {
                console.log('have no more ...')
                clearInterval(id)
            })
        }, 3000)
    }

    function getNextArticle(currArticle) {
        return new Promise((resolve, reject) => {
            let nextArticle;
            if (currArticle === null) {
                const articleList = document.getElementById('scroller').getElementsByTagName('article')
                nextArticle = articleList.length === 0 ? null : articleList[0]
            } else {
                const nextContent = currArticle.parentElement.parentElement.nextElementSibling
                if (nextContent === null || nextContent === undefined) {
                    debugger
                    nextArticle = null
                } else {
                    const nextArticleList = nextContent.getElementsByTagName('article')
                    nextArticle = nextArticleList.length === 0 ? null : nextArticleList[0]
                }
            }

            if (nextArticle === null || nextArticle === undefined) {
                reject()
            }
            // 页面滚动
            nextArticle.scrollIntoView()
            setTimeout(() => {
                resolve(nextArticle)
            }, 1000)
        })
    }

    function judgeDelete(article) {
        const content = article.outerText
        return content.search('此内容无法访问') !== -1
            || content.search('此微博已被作者删除') !== -1
            || content.search('此微博已不可见') !== -1
    }

    function deleteThis(article) {
        // 先判断header
        const headerList = article.getElementsByTagName('header')
        if (headerList.length !== 1) {
            console.log('header数量不符合预期, 跳过删除')
            return
        }

        const header = headerList[0]
        const menuIcon = header.getElementsByTagName('i')[0]
        menuIcon.click()

        // 等待对话框加载
        wait(() => {
            return header.getElementsByClassName('woo-pop-wrap-main')
        }).then((menuList) => {
            const menu = menuList[0]
            const delDiv = menu.children[6]
            delDiv.click()

            // 等待删除框加载
            wait(() => {
                return document.getElementById('app')
                    .getElementsByClassName('woo-button-main woo-button-flat woo-button-default woo-button-m woo-button-round woo-dialog-btn')
            }).then((confirmBtnList) => {
                setTimeout(() => {
                    confirmBtnList[0].click()
                }, 500)
            })
        })
    }

    function wait(finder) {
        let maxWaitTime = 5 * 1000
        return new Promise((resolve, reject) => {
            const intervalId = setInterval(() => {
                try {
                    const result = finder()
                    if (result !== null && result !== undefined && result.length !== 0) {
                        clearInterval(intervalId)
                        resolve(result)
                    }
                } catch (e) {

                }
                maxWaitTime = maxWaitTime - 200
                if (maxWaitTime <= 0) {
                    reject('超时')
                }
            }, 200)
        })
    }
}