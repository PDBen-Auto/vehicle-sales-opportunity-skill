import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=path.dirname(fileURLToPath(import.meta.url)),out=path.resolve(root,'../输出'),data=JSON.parse(await fs.readFile(path.join(out,'data/dataset.json'),'utf8'));
const qa=path.join(root,'qa');await fs.mkdir(qa,{recursive:true});
const wb=Workbook.create();
const sheets=Object.fromEntries(['概览','车型估算','参数','批次计算','车型目录','补充证据','来源台账','缺口与方法'].map(n=>[n,wb.worksheets.add(n)]));
const green='#244D3E',amber='#8C6225',ink='#263E34';
function setup(sheet,title,headers,rows,widths){
 const cols=headers.length,n=rows.length+4;
 sheet.showGridLines=false;
 sheet.getRangeByIndexes(0,0,n,cols).format.font={name:'Arial',size:10,color:ink};
 sheet.getRange('A2').values=[[title]];sheet.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:ink};
 sheet.getRangeByIndexes(3,0,1,cols).values=[headers];
 if(rows.length)sheet.getRangeByIndexes(4,0,rows.length,cols).values=rows;
 let head=sheet.getRangeByIndexes(3,0,1,cols);head.format={fill:green,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:30,wrapText:true};
 sheet.getRangeByIndexes(4,0,Math.max(1,rows.length),cols).format.rowHeight=32;
 sheet.getRangeByIndexes(3,0,Math.max(1,rows.length+1),cols).format.verticalAlignment='center';
 for(let i=0;i<cols;i++)sheet.getRangeByIndexes(0,i,n,1).format.columnWidthPx=widths[i]||140;
 if(rows.length){sheet.tables.add(sheet.getRangeByIndexes(3,0,rows.length+1,cols).address||`A4:${col(cols)}${n}`,true,'UtvTable'+Object.keys(sheets).indexOf(sheet));}
 sheet.freezePanes.freezeRows(4);
}
function col(n){let s='';for(;n;n=Math.floor((n-1)/26))s=String.fromCharCode(65+(n-1)%26)+s;return s;}
// Table names are created using stable worksheet-specific indexes below.
let tableIndex=0;
function grid(name,title,headers,rows,widths){
 const s=sheets[name],cols=headers.length,n=rows.length+4;s.showGridLines=false;
 s.getRangeByIndexes(0,0,n,cols).format.font={name:'Arial',size:10,color:ink};
 s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:ink};
 s.getRangeByIndexes(3,0,1,cols).values=[headers];if(rows.length)s.getRangeByIndexes(4,0,rows.length,cols).values=rows;
 s.getRangeByIndexes(3,0,1,cols).format={fill:green,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},rowHeight:32,wrapText:true};
 if(rows.length)s.getRangeByIndexes(4,0,rows.length,cols).format.rowHeight=32;
 s.getRangeByIndexes(3,0,rows.length+1,cols).format.verticalAlignment='center';
 for(let i=0;i<cols;i++)s.getRangeByIndexes(0,i,n,1).format.columnWidthPx=widths[i]||150;
 if(rows.length)s.tables.add(`A4:${col(cols)}${n}`,true,'UtvTable'+(++tableIndex));
 s.freezePanes.freezeRows(4);return s;
}
const params=[['快照年份',2026,'固定研究快照年份'],['基准兑现系数',.90,'研究假设，非实证存活率'],['基准年保留系数',.93,'研究假设，非实证存活率'],['更严兑现系数',.80,'压力情景'],['更严年保留系数',.88,'压力情景'],['较缓兑现系数',.95,'压力情景'],['较缓年保留系数',.97,'压力情景']];
const ps=grid('参数','估算参数（可编辑假设）',['参数','数值','含义'],params,[240,150,520]);
ps.getRange('B6:B11').setNumberFormat('0%');ps.getRange('B5:B11').format.fill='#FFF1D1';
ps.getRange('A14').values=[['公式：历史批次数 × 兑现系数 × 年保留系数 ^ 压力车龄']];
ps.getRange('A16').values=[['压力车龄按最早年款与最早销售年中更早者计算；不补新销量、遗漏年款或未召回VIN。']];
ps.getRange('A18').values=[['区间是研究者参数压力情景，不是置信区间或可证明的存量上下界。']];
ps.tabColor='#8C9E85';
const comps=data.components,cs=grid('批次计算','已选历史批次与情景计算（低置信度）',['国家','车型ID','来源ID','窗口起年','窗口止年','最早销售年','压力车龄','历史批次数','基准未取整','更严未取整','较缓未取整','公告日','数量原文','来源URL','窗口性质'],comps.map(c=>[c.country,c.model_id,c.source_id,c.model_year_start,c.model_year_end,c.oldest_sale_year,null,c.historical_units,null,null,null,c.recall_date,c.units_text,c.source_url,c.window_basis]),[70,330,140,110,110,110,110,130,140,140,140,120,450,520,220]);
for(let i=0;i<comps.length;i++){let r=i+5;cs.getRange(`G${r}`).formulas=[[`=MAX(0,'参数'!$B$5-MIN(D${r},F${r}))`]];cs.getRange(`I${r}:K${r}`).formulas=[[`=H${r}*'参数'!$B$6*POWER('参数'!$B$7,G${r})`,`=H${r}*'参数'!$B$8*POWER('参数'!$B$9,G${r})`,`=H${r}*'参数'!$B$10*POWER('参数'!$B$11,G${r})`]];}
cs.getRange(`H5:K${comps.length+4}`).setNumberFormat('#,##0.00');cs.getRange(`H5:H${comps.length+4}`).setNumberFormat('#,##0');
const results=data.scenarios,ms=grid('车型估算','分国家车型与批次保守情景（台）',['国家','品牌','车型或明确统计组','条目类型','用途','历史批次数','批次基准','更严情景','较缓情景','全车型保有量','该国身份','来源窗口','说明','来源ID','父统计组','基准未取整','更严未取整','较缓未取整'],results.map(r=>[r.country,r.make,r.model,r.aggregation_level==='source_group'?'合并组':'系列',r.category,r.historical_affected_units??'unknown',r.conservative_batch_scenario??'unknown',r.severe_batch_scenario??'unknown',r.less_severe_batch_scenario??'unknown','unknown',r.market_presence,r.cohort_window,r.notes,r.source_ids,r.parent_id,null,null,null]),[72,150,350,100,100,125,130,130,130,135,240,250,650,360,310,145,145,145]);
const end=comps.length+4;
for(let i=0;i<results.length;i++){const x=results[i],r=i+5;if(x.historical_affected_units==null)continue;
 for(const [dest,source] of [['P','I'],['Q','J'],['R','K']])ms.getRange(`${dest}${r}`).formulas=[[`=SUMIFS('批次计算'!$${source}$5:$${source}$${end},'批次计算'!$A$5:$A$${end},A${r},'批次计算'!$B$5:$B$${end},"${x.canonical_model_id}")`]];
 ms.getRange(`G${r}:I${r}`).formulas=[[`=FLOOR(P${r},IF(P${r}>=1000,100,IF(P${r}>=100,10,1)))`,`=FLOOR(Q${r},IF(Q${r}>=1000,100,IF(Q${r}>=100,10,1)))`,`=CEILING(R${r},IF(R${r}>=1000,100,IF(R${r}>=100,10,1)))`]];
}
ms.getRange(`F5:I${results.length+4}`).setNumberFormat('#,##0');ms.getRange(`G5:I${results.length+4}`).format.font.color=amber;ms.getRange(`P5:R${results.length+4}`).setNumberFormat('#,##0.00');ms.freezePanes.freezeColumns(3);ms.tabColor=green;
grid('车型目录','系列、子车型与来源合并组',['车型ID','品牌','名称','用途','性质','父统计组','全量状态','说明','来源ID'],data.models.map(m=>[m.id,m.brand,m.name,m.category,m.group?'来源合并组':m.parent_id?'合并组子车型':m.catalog_only?'目录候选':'系列',''+(m.parent_id||''),'unknown',m.notes,m.source_ids.join(';')]),[330,170,350,110,140,330,130,650,400]);
grid('补充证据','重叠、混合与排除证据（不再加总）',['公告日','记录ID','公告标题','数量原文','处理','来源URL'],data.evidence_pool.map(r=>[r.date,r.recall_id,r.title,r.units_text,r.decision,r.source_url]),[130,120,660,520,650,650]);
grid('来源台账','来源与本地快照（检索日2026-11-17）',['来源ID','发布方','发布日期','标题','URL','指标','快照路径','SHA-256','说明'],data.sources.map(s=>[s.source_id,s.publisher,s.published_at,s.title,s.url,s.metric,s.local_snapshot,s.checksum_sha256,s.notes]),[160,160,125,650,650,300,330,520,650]);
const gaps=grid('缺口与方法','覆盖边界与后续输入',['范围','状态','缺口','所需输入'],data.gaps.map(g=>[g.area,g.status,g.gap,g.next_input]),[180,140,760,650]);
gaps.getRange('C5:D13').format.wrapText=true;gaps.getRange('A5:D13').format.rowHeight=64;
const ss=sheets['概览'];ss.showGridLines=false;ss.tabColor=green;ss.getRange('A1:H26').format.font={name:'Arial',size:11,color:ink};ss.getRange('A2').values=[['北美 UTV 保有量研究 · 首版']];ss.getRange('A2').format.font={size:16,bold:true,color:ink};ss.getRange('A4').values=[['研究截止：2026-11-17。全部车型的全量当前保有量未知。']];ss.getRange('A5').values=[['数字仅为已知历史批次的在用压力情景，没有补齐遗漏年款、未召回VIN与新增销售。']];
ss.getRange('A7:F7').values=[['国家','可计算批次条目','全量当前保有量','已取得VIO条数','覆盖','说明']];ss.getRange('A7:F7').format={fill:green,font:{name:'Arial',bold:true,color:'#FFFFFF'},rowHeight:32};
for(let i=0;i<3;i++){let c=['US','CA','MX'][i],r=i+8;ss.getRange(`A${r}:F${r}`).values=[[c,null,'unknown',0,'partial',c==='US'?'含系列与合并组；不可作为车型销量排名':c==='CA'?'仅采用公告明确另列的加拿大数量':'仅Wildcat混合组可计算，其余数量缺失']];ss.getRange(`B${r}`).formulas=[[`=COUNTIFS('车型估算'!$A$5:$A$${results.length+4},A${r},'车型估算'!$F$5:$F$${results.length+4},">=0")`]];}
ss.getRange('A13:B16').values=[['跨市场目录条目',data.counts.catalog_entries],['明确来源合并组',data.counts.source_group_entries],['单独命名系列条目',data.counts.named_series_entries],['已选历史批次组件',data.counts.components]];
ss.getRange('A19').values=[['“保守基准 / 更严 / 较缓”均是研究假设，不是官方数据或统计置信区间。']];ss.getRange('A21').values=[['合并组子车型保持未知；禁止把一组合计重复填入每个子车型。']];ss.getRange('A23').values=[['可在“参数”修改基准假设，批次与车型公式会重算；CSV / HTML为独立快照。']];
for(let [c,w] of [['A',185],['B',160],['C',180],['D',160],['E',110],['F',460],['G',100],['H',100]])ss.getRange(`${c}1:${c}26`).format.columnWidthPx=w;ss.getRange('A8:F10').format.rowHeight=36;
wb.recalculate();
// Meaningful sensitivity check in the same calculation engine, followed by restoration.
const initial=ms.getRange('G5').values[0][0];ps.getRange('B7').values=[[.90]];wb.recalculate();const changed=ms.getRange('G5').values[0][0];if(!(Number(changed)<Number(initial)))throw Error('Parameter sensitivity did not update model result');ps.getRange('B7').values=[[.93]];wb.recalculate();const restored=ms.getRange('G5').values[0][0];if(Number(restored)!==Number(initial))throw Error('Parameter restoration mismatch');
const inspect=await wb.inspect({kind:'table',range:'车型估算!A4:J7',include:'values,formulas',tableMaxRows:4,tableMaxCols:10,maxChars:2200});
await fs.writeFile(path.join(qa,'workbook-inspect.ndjson'),inspect.ndjson);
const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!',options:{useRegex:true,maxResults:50},maxChars:2000});await fs.writeFile(path.join(qa,'workbook-error-scan.ndjson'),scan.ndjson);
for(const n of Object.keys(sheets)){const preview=await wb.render({sheetName:n,range:n==='概览'?'A1:F16':n==='参数'?'A1:C12':n==='缺口与方法'?'A1:D8':n==='车型估算'?'A1:I10':n==='批次计算'?'A1:K10':'A1:F9',scale:1,format:'png'});await fs.writeFile(path.join(qa,'sheet-'+n+'.png'),new Uint8Array(await preview.arrayBuffer()));}
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(path.join(out,'北美UTV车型保有量保守情景-20261117.xlsx'));
await fs.writeFile(path.join(qa,'workbook-sensitivity.json'),JSON.stringify({initial,changed,restored,passed:true,engine:'artifact-tool',native_excel_recalculation:'not tested'},null,2));console.log(JSON.stringify({sheets:8,initial,changed,restored,exported:true}));
