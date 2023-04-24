const fs = require('fs');
const path =  require('path');
const statusInvest = require('statusinvest');

var tickerName = process.argv[2];

const absolutePath = path.resolve('.') + '/data/' + tickerName + '.json';

const saveFile = async () => {

    const res = await statusInvest.getStockHistoricalInfo({ 
        ticker : tickerName 
    })

    fs.writeFile(absolutePath, JSON.stringify(res), (err) => {
        if(err){
            console.log(err);
        }
    });
}

saveFile();