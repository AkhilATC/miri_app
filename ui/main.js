const electron = require('electron');
const url =  require('url');
const path = require('path');

const {app,BrowserWindow, Menu } = require('electron');
const { webContents } = require("electron");


let miRiMainWindow;
let productWindow;
let billWindow;
console.log("here")
//Listen app is on
app.on('ready',function(){
    // assign miri window
    miRiMainWindow = new BrowserWindow({icon: __dirname + '/src/assets/icon/miri.png'});
    // bind miri window with html
    miRiMainWindow.loadURL(url.format({
        pathname:path.join(__dirname,'src/miri_index.html'),
        protocol:'file:',
        slashes:true
    }))
    const mainMenu = Menu.buildFromTemplate(miRiMenuData);
    Menu.setApplicationMenu(mainMenu);
//    miRiMainWindow.webContents.openDevTools();
    
})
app.on('close',function(){
productWindow.close()
    miRiMainWindow = null;

    productWindow = null;
    billWindow = null;
    app.quit();
})

// Menu tab for miRi

function loadAddproduct(){
    productWindow = new BrowserWindow({
        height:550,
        width:400,
        title:'add product',
        resizable: false,
        transparent: true,
        autoHideMenuBar: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
            
        }
    });
    productWindow.loadURL(url.format({
        pathname:path.join(__dirname,'src/add_product.html'),
        protocol:'file:',
        slashes:true
    }))
//    productWindow.webContents.openDevTools();
}
function loadBillWindow(){

    billWindow = new BrowserWindow({
//        height:550,
//        width:400,
        title:'Generate bill',
        resizable: true,
        transparent: true,
        autoHideMenuBar: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true

        }
    });
    billWindow.loadURL(url.format({
        pathname:path.join(__dirname,'src/generate_bill.html'),
        protocol:'file:',
        slashes:true
    }))
     billWindow.webContents.openDevTools();

}
const miRiMenuData = [{
    label: 'Add',
    submenu:[
        {
            label:'Product',
            click(){
                loadAddproduct();
            }
        },
        {
            label: 'Ventor'
        }
    ]
     
    },{
    label : 'Export',
    submenu : [
                {
                label:'Bill',
                click(){
                loadBillWindow();
                    }
                }
             ]

    }]