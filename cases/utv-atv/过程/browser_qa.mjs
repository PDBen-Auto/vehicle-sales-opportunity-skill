import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {chromium} from 'playwright';

const root=path.dirname(fileURLToPath(import.meta.url)),out=path.resolve(root,'../输出'),qa=path.join(root,'qa');
const report={as_of_date:'2026-11-17',runtime:'isolated Playwright / direct file URL',checks:[],errors:[],native_excel_recalculation:'not tested',archive_status:'not published: current conversation has no confirmed business project',source_task_id:'01a1d30f-d97a-7532-9cae-759ea260d0fa'};
let browser,context,page;
function check(name,value,detail){report.checks.push({name,passed:!!value,...(detail?{detail}:{})});if(!value)throw new Error(name+': '+JSON.stringify(detail));}
async function snapshot(name,fullPage=true){await page.screenshot({path:path.join(qa,name+'.png'),fullPage});}
async function clickTab(tab){await page.locator(`[data-tab="${tab}"]`).click();}
async function rows(){return await page.locator('#rows tr').count();}
async function country(c){await page.locator(`[data-country="${c}"]`).click();}
async function resetFilters(){await page.locator('#search').fill('');for(const id of ['brand','category'])await page.locator('#'+id).selectOption('');await page.locator('#scope').selectOption('quantified');}
try{
 // Resolve an installed isolated Chromium; the package's default headless build is absent.
 const browserRoot=path.join(process.env.LOCALAPPDATA,'ms-playwright');
 const installed=(await fs.readdir(browserRoot)).filter(n=>/^chromium-\d+$/.test(n)).sort((a,b)=>Number(b.split('-')[1])-Number(a.split('-')[1]));
 let executablePath;
 for(const name of installed){const candidate=path.join(browserRoot,name,'chrome-win64/chrome.exe');try{await fs.access(candidate);executablePath=candidate;break;}catch{}}
 if(!executablePath)throw Error('No installed isolated Chromium executable');
 report.browser_executable=executablePath;
 browser=await chromium.launch({headless:true,executablePath});
 context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
 page=await context.newPage();
 const pageErrors=[],consoleErrors=[],remoteRequests=[];
 page.on('pageerror',e=>pageErrors.push(e.message));page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text());});page.on('request',r=>{if(/^https?:/.test(r.url()))remoteRequests.push(r.url());});
 await page.goto(pathToFileURL(path.join(out,'北美UTV保有量研究-20261117.html')).href);
 await page.locator('#rows tr').first().waitFor();
 check('initial_us_63_entries',(await page.locator('#result-count').textContent()).includes('63 条'));
 check('initial_15_rows',await rows()===15);
 check('full_vio_remains_unknown',(await page.locator('#stats').textContent()).includes('全车型当前保有量未知'));
 await snapshot('desktop-1440');
 check('desktop_no_body_overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
 check('visible_images_load',await page.locator('#rows img').evaluateAll(es=>es.filter(e=>e.getBoundingClientRect().top<innerHeight).every(e=>e.complete&&e.naturalWidth>0)));
 await page.locator('#search').fill('RZR');
 check('search_rzr',await rows()>0&&(await page.locator('#rows').textContent()).includes('RZR'));
 await page.locator('#search').fill('no-such-model-987');
 check('empty_search_state',(await page.locator('#rows').textContent()).includes('没有匹配条目'));
 await resetFilters();await page.locator('#brand').selectOption('Honda');
 check('brand_filter_honda',await rows()===3);
 await page.locator('#category').selectOption('运动');
 check('category_filter_sport',await rows()===1&&(await page.locator('#rows').textContent()).includes('Talon'));
 await resetFilters();await country('CA');
 check('canada_15_entries',(await page.locator('#result-count').textContent()).includes('15 条'));
 await country('MX');
 check('mexico_one_group',await rows()===1&&(await page.locator('#rows').textContent()).includes('Wildcat Trail / Sport'));
 check('mexico_historical_100',(await page.locator('#rows td').nth(3).textContent())==='100');
 await country('US');await page.locator('#scope').selectOption('all');
 check('all_124_entries',(await page.locator('#result-count').textContent()).includes('124 条'));
 const first=await page.locator('#rows .modelname').first().textContent();await page.locator('#next').click();
 check('pagination_changes_rows',(await page.locator('#page-label').textContent())==='2 / 9'&&(await page.locator('#rows .modelname').first().textContent())!==first);
 await page.locator('#prev').click();check('pagination_returns',(await page.locator('#rows .modelname').first().textContent())===first);
 await page.locator('#scope').selectOption('unknown');check('unknown_61_entries',(await page.locator('#result-count').textContent()).includes('61 条'));
 await page.locator('#scope').selectOption('groups');check('20_explicit_groups',(await page.locator('#result-count').textContent()).includes('20 条'));
 await resetFilters();await page.locator('#search').fill('XP 1000 / XP 4');await page.locator('#rows .open').click();
 check('detail_opens',await page.locator('#detail').evaluate(e=>e.open));
 check('rzr_two_nonoverlap_components',await page.locator('#detail .cohort').count()===2);
 check('rzr_detail_correct_baseline',(await page.locator('#detail .detailvals strong').first().textContent())==='52,600');
 await snapshot('desktop-detail',false);await page.keyboard.press('Escape');
 check('escape_closes_modal',!(await page.locator('#detail').evaluate(e=>e.open)));
 await page.locator('#scope').selectOption('all');await page.locator('#search').fill('Rhino 450');
 await page.locator('#rows .modelbtn').filter({hasText:'Rhino 450'}).last().click();
 check('child_has_no_allocated_number',(await page.locator('#detail .detailvals strong').first().textContent())==='未估');
 await page.locator('#detail [data-parent]').click();
 check('parent_navigation_correct',(await page.locator('#detail-title').textContent()).includes('450 / 660 / 700')&&(await page.locator('#detail .detailvals strong').first().textContent())==='24,500');
 await page.locator('#close').click();
 await resetFilters();await page.locator('#search').fill('XP 1000 / XP 4');
 const baseline=await page.locator('#rows .value').first().textContent();
 await clickTab('method');
 await page.locator('#retentionRate').evaluate(el=>{el.value='0.90';el.dispatchEvent(new Event('input',{bubbles:true}));});
 check('parameter_status_updates',(await page.locator('#param-status').textContent()).includes('参数已修改'));
 await clickTab('models');const changed=await page.locator('#rows .value').first().textContent();check('html_sensitivity',baseline==='52,600'&&changed==='38,200',{baseline,changed});
 const dlPromise=page.waitForEvent('download');await page.locator('#export').click();const dl=await dlPromise;const exportPath=path.join(qa,'filtered-export.csv');await dl.saveAs(exportPath);let exported=await fs.readFile(exportPath,'utf8');
 check('filtered_export_matches_adjusted_value',exported.includes('38200')&&exported.includes('unknown')&&exported.includes('0.9')&&exported.trim().split('\n').length===2);
 await clickTab('method');await page.locator('#reset').click();await clickTab('models');check('html_sensitivity_restores',(await page.locator('#rows .value').first().textContent())===baseline);
 await clickTab('evidence');check('coverage_gaps_visible',await page.locator('.gaprow').count()===9);await page.locator('#source-count').click();check('105_source_rows',await page.locator('#sources tr').count()===105);
 await snapshot('desktop-evidence');await page.locator('#source-count').click();
 await clickTab('models');await resetFilters();
 await page.setViewportSize({width:390,height:844});
 check('mobile_no_body_overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),await page.evaluate(()=>({body:document.documentElement.scrollWidth,viewport:innerWidth})));
 check('mobile_numeric_card_visible',await page.locator('#rows .value').first().evaluate(e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth;}));
 check('mobile_main_table_has_no_horizontal_scroll',await page.locator('#models .tablebox').evaluate(e=>e.scrollWidth<=e.clientWidth));
 await page.locator('#search').blur();await page.evaluate(()=>window.scrollTo(0,0));await snapshot('mobile-390');
 await page.locator('#rows .open').first().click();check('mobile_modal_fits',await page.locator('#detail').evaluate(e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight;}));
 await snapshot('mobile-detail',false);await page.locator('#close').click();
 await clickTab('method');check('mobile_method_no_overflow',await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));await snapshot('mobile-method');
 check('no_page_errors',pageErrors.length===0,pageErrors);check('no_console_errors',consoleErrors.length===0,consoleErrors);check('no_remote_runtime_requests',remoteRequests.length===0,remoteRequests);
 report.passed=true;
}catch(e){report.passed=false;report.errors.push(e.stack||String(e));if(page)await snapshot('failed-state').catch(()=>{});}
finally{
 if(context){for(const p of context.pages())await p.close();report.closed_all_test_pages=context.pages().length===0;await context.close();}
 if(browser){await browser.close();report.closed_owned_browser=true;}
 await fs.writeFile(path.join(out,'data/delivery_qa.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report));
}
if(!report.passed)process.exitCode=1;
