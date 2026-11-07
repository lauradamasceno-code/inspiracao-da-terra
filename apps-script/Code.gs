/**
 * Lemaréz Gestão — servidor (Google Apps Script)
 * Guarda tudo nas abas app_clientes, app_vendas, app_custos, app_produtos e app_catalogo
 * da planilha Google em que este script foi criado.
 */

var SCHEMA = {
  clientes: ['id', 'nome', 'cpf', 'endereco', 'email', 'telefone', 'nascimento', 'consentimento', 'criado'],
  vendas: ['id', 'data', 'desc', 'cliente', 'tipo', 'cat', 'produto', 'frag', 'extra', 'qtd', 'pag', 'valor'],
  custos: ['id', 'data', 'desc', 'tipo', 'cat', 'pag', 'valor'],
  produtos: ['id', 'nome', 'cat', 'preco', 'custo'],
  catalogo: ['id', 'codigo', 'nome', 'marca', 'genero']
};
var MAX_LEN = 500;

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Lemaréz Gestão')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function sheet_(tab) {
  if (!SCHEMA[tab]) throw new Error('Aba inválida: ' + tab);
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var name = 'app_' + tab;
  var sh = ss.getSheetByName(name);
  if (!sh) {
    var h = SCHEMA[tab];
    sh = ss.insertSheet(name);
    sh.getRange(1, 1, sh.getMaxRows(), h.length).setNumberFormat('@'); // tudo como texto: CPF e datas não são alterados
    sh.getRange(1, 1, 1, h.length).setValues([h]).setFontWeight('bold').setBackground('#0b2a1f').setFontColor('#ffffff');
    sh.setFrozenRows(1);
  }
  return sh;
}

function toRow_(tab, obj) {
  return SCHEMA[tab].map(function (k) {
    var v = obj[k];
    if (v === null || v === undefined) return '';
    return String(v).substring(0, MAX_LEN);
  });
}

function findRow_(sh, id) {
  var last = sh.getLastRow();
  if (last < 2) return -1;
  var ids = sh.getRange(2, 1, last - 1, 1).getValues();
  for (var i = 0; i < ids.length; i++) {
    if (String(ids[i][0]) === String(id)) return i + 2;
  }
  return -1;
}

function withLock_(fn) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    return fn();
  } finally {
    lock.releaseLock();
  }
}

/** Lê todas as abas e devolve um objeto { clientes: [...], vendas: [...], ... } */
function api_load() {
  var out = {};
  Object.keys(SCHEMA).forEach(function (tab) {
    var sh = sheet_(tab);
    var h = SCHEMA[tab];
    var last = sh.getLastRow();
    var list = [];
    if (last >= 2) {
      var vals = sh.getRange(2, 1, last - 1, h.length).getValues();
      vals.forEach(function (row) {
        if (!row[0]) return;
        var o = {};
        h.forEach(function (k, i) { o[k] = row[i] === null || row[i] === undefined ? '' : String(row[i]); });
        list.push(o);
      });
    }
    out[tab] = list;
  });
  return out;
}

/** Cria ou atualiza uma linha (pelo id). */
function api_save(tab, obj) {
  return withLock_(function () {
    var sh = sheet_(tab);
    var row = toRow_(tab, obj);
    if (!row[0]) throw new Error('Registro sem id.');
    var r = findRow_(sh, row[0]);
    if (r < 0) r = sh.getLastRow() + 1;
    var rng = sh.getRange(r, 1, 1, row.length);
    rng.setNumberFormat('@');
    rng.setValues([row]);
    return true;
  });
}

/** Grava várias linhas novas de uma vez (ignora ids que já existem). */
function api_saveMany(tab, list) {
  return withLock_(function () {
    var sh = sheet_(tab);
    var last = sh.getLastRow();
    var have = {};
    if (last >= 2) {
      sh.getRange(2, 1, last - 1, 1).getValues().forEach(function (r) { have[String(r[0])] = true; });
    }
    var rows = [];
    (list || []).forEach(function (o) {
      var row = toRow_(tab, o);
      if (row[0] && !have[row[0]]) { rows.push(row); have[row[0]] = true; }
    });
    if (rows.length) {
      var rng = sh.getRange(last + 1, 1, rows.length, rows[0].length);
      rng.setNumberFormat('@');
      rng.setValues(rows);
    }
    return rows.length;
  });
}

/** Apaga uma linha. */
function api_delete(tab, id) {
  return withLock_(function () {
    var sh = sheet_(tab);
    var r = findRow_(sh, id);
    if (r > 0) sh.deleteRow(r);
    return true;
  });
}

/** Exclui um cliente (LGPD) e remove o vínculo dele nas vendas. */
function api_delCliente(id) {
  return withLock_(function () {
    var sc = sheet_('clientes');
    var r = findRow_(sc, id);
    if (r > 0) sc.deleteRow(r);
    var sv = sheet_('vendas');
    var last = sv.getLastRow();
    if (last >= 2) {
      var col = SCHEMA.vendas.indexOf('cliente') + 1;
      var rng = sv.getRange(2, col, last - 1, 1);
      var vals = rng.getValues();
      var changed = false;
      for (var i = 0; i < vals.length; i++) {
        if (String(vals[i][0]) === String(id)) { vals[i][0] = ''; changed = true; }
      }
      if (changed) rng.setValues(vals);
    }
    return true;
  });
}
