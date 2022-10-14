// 現在の時刻を示すDateオブジェクトのインスタンスを作成
const now = new Data()

function getDate() {
    let year = now.getFullYear(); //年の取得
    let month = now.getMonth(); + 1 //月の取得(+1の理由は、取得する結果が0〜11のため)
    let date = now.getDate(); //日の取得
    let today = year + "-" + month + "-" + date
    return today //YYYY-MM-DDのフォーマットで返却
}