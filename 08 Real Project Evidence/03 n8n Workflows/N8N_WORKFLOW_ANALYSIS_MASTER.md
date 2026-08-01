# N8N Workflow Analysis Master

Definition-based analysis of all unique GH-X workflow exports.

**Workflows analyzed:** 23 exports + 1 local stub
**Production Ready count:** 0

## Design + Reel Prompt Generator
- **Group:** B
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 6 / 6
- **Integrations:** Airtable, Code, Schedule Trigger, Split In Batches
- **AI:** None detected
- **Purpose:** On a schedule, search records, build design/reel prompts in Code nodes, and update Airtable.
- **Plain English:** Starts on a schedule (`Schedule Trigger`). Airtable `search` via `Search records`. Processes records in batches (`Loop Over Items`). Transforms/prepares data in Code node `Code in JavaScript`. Transforms/prepares data in Code node `Batch complete`. Airtable `update` via `Update record`.
- **Doc:** `./Project-B_Listing_and_Prompt_Generation/Design-Reel-Prompt-Generator/README.md`

## GH-X OpenAI Image Generator
- **Group:** C
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 10 / 9
- **Integrations:** Airtable, Code, Google Drive, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger
- **AI:** HTTP · OpenAI Images → OpenAI Images
- **Purpose:** On a schedule, find design-ready rows, call OpenAI Images via HTTP, store via Google Drive, and update Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Cover Image Run`). Airtable `search` via `Airtable · Search One Ready To Design`. Transforms/prepares data in Code node `Code · Build OpenAI Image Body`. HTTP request via `HTTP · OpenAI Images` (OpenAI Images). Transforms/prepares data in Code node `Code · Response To Binary`. Branches with an IF check (`Filter · Image OK`). Uses Google Drive (`Google Drive · Upload Cover`). Airtable `update` via `Airtable · Log Error`. Transforms/prepares data in Code node `Code · Merge Drive URL`. Airtable `update` via `Airtable · Update By Record Id`.
- **Doc:** `./Project-C_Visual_Asset_Generation/GH-X-OpenAI-Image-Generator/README.md`

## GHX-00-Error-Alerts
- **Group:** H
- **Complexity:** Beginner
- **Status:** Functional Build
- **Nodes / edges:** 5 / 4
- **Integrations:** Code, Error Trigger, HTTP Request, IF, NoOp
- **AI:** None detected
- **Purpose:** Catch n8n workflow errors and route them through filtering/alerting logic.
- **Plain English:** Starts when another workflow errors (`Error Trigger`). Transforms/prepares data in Code node `Code · Format Payload`. Branches with an IF check (`Filter · Webhook URL Set`). HTTP request via `HTTP · POST Alert`. No-op placeholder (`No Op · Skip Alert`).
- **Doc:** `./Project-H_Reliability_and_Alerts/GHX-00-Error-Alerts/README.md`

## GHX-01-Idea-Intelligence
- **Group:** A
- **Complexity:** Beginner
- **Status:** Functional Build
- **Nodes / edges:** 5 / 4
- **Integrations:** Airtable, Code, HTTP Request, OpenAI (via HTTP), Schedule Trigger
- **AI:** HTTP · OpenAI Chat → OpenAI Chat
- **Purpose:** On a schedule, generate product ideas (OpenAI HTTP) and create Airtable product records.
- **Plain English:** Starts on a schedule (`Schedule · Weekly Ideas`). Transforms/prepares data in Code node `Code · Build OpenAI Body`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Parse Ideas`. Airtable `create` via `Airtable · Create Product`.
- **Doc:** `./Project-A_Idea_Intelligence/GHX-01-Idea-Intelligence/README.md`

## GHX-03-Etsy-Metricool-Handoff
- **Group:** D
- **Complexity:** Beginner
- **Status:** Functional Build
- **Nodes / edges:** 4 / 3
- **Integrations:** Airtable, Code, Schedule Trigger
- **AI:** None detected
- **Purpose:** On a schedule, search ready rows and prepare/save draft handoff fields in Airtable for publishing prep.
- **Plain English:** Starts on a schedule (`Schedule · Publishing Prep`). Airtable `search` via `Airtable · Search Ready Rows`. Transforms/prepares data in Code node `Code · Build Draft JSON`. Airtable `update` via `Airtable · Save Drafts`.
- **Doc:** `./Project-D_Commerce_Publish_Etsy/GHX-03-Etsy-Metricool-Handoff/README.md`

## GHX-03B-Product-File-Uploader
- **Group:** C
- **Complexity:** Advanced
- **Status:** Functional Build
- **Nodes / edges:** 22 / 29
- **Integrations:** Airtable, Code, Google Drive, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Set, Split In Batches, Switch
- **AI:** HTTP · OpenAI Product Blueprint → OpenAI Chat, HTTP · OpenAI Product Image → OpenAI Images
- **Purpose:** On a schedule, build product blueprints/images via OpenAI HTTP and write product file URLs or errors to Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Product File Run`). Sets fields (`Set · Load Product Gen Config`). Transforms/prepares data in Code node `Code · Setup Config`. Airtable `search` via `Airtable · Search Needs Product File`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Prepare Product Job`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Job OK`). HTTP request via `HTTP · OpenAI Product Blueprint` (OpenAI Chat). Airtable `update` via `Airtable · Log File Error`. Transforms/prepares data in Code node `Code · Parse Product Blueprint`. Branches with an IF check (`Filter · Blueprint OK`). Routes with a Switch (`Switch · Output Format`). Transforms/prepares data in Code node `Code · Generate Product File · PDF`. HTTP request via `HTTP · OpenAI Product Image` (OpenAI Images). Branches with an IF check (`Filter · Product Binary OK`). Transforms/prepares data in Code node `Code · Image To Binary`. Uses Google Drive (`Google Drive · Upload Product File`).
- **Doc:** `./Project-C_Visual_Asset_Generation/GHX-03B-Product-File-Uploader/README.md`

## GHX-04-Mockup-Generator
- **Group:** C
- **Complexity:** Advanced
- **Status:** Functional Build
- **Nodes / edges:** 15 / 17
- **Integrations:** Airtable, Code, Google Drive, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Split In Batches
- **AI:** HTTP · OpenAI Chat → OpenAI Chat, HTTP · OpenAI Images → OpenAI Images
- **Purpose:** On a schedule, process mockup queue rows with OpenAI Chat + Images, store assets (Google Drive), and update Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Mockup Run`). Airtable `search` via `Airtable · Search Mockup Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Mockup Chat Body`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Parse Mockup Prompt`. Branches with an IF check (`Filter · Prompt OK`). HTTP request via `HTTP · OpenAI Images` (OpenAI Images). Airtable `update` via `Airtable · Update Error`. Transforms/prepares data in Code node `Code · Image To Binary`. Branches with an IF check (`Filter · Image OK`). Uses Google Drive (`Google Drive · Upload Mockup`). Transforms/prepares data in Code node `Code · Merge Drive Link`. Airtable `update` via `Airtable · Update Success`.
- **Doc:** `./Project-C_Visual_Asset_Generation/GHX-04-Mockup-Generator/README.md`

## GHX-05-Social-Asset-Generator
- **Group:** C
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 10 / 11
- **Integrations:** Airtable, Code, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Split In Batches
- **AI:** HTTP · OpenAI Chat → OpenAI Chat
- **Purpose:** On a schedule, process social queue rows with OpenAI Chat via HTTP and update Airtable success/error fields.
- **Plain English:** Starts on a schedule (`Schedule · Social Run`). Airtable `search` via `Airtable · Search Social Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Social Chat Body`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Parse Social JSON`. Branches with an IF check (`Filter · Parse OK`). Airtable `update` via `Airtable · Update Success`. Airtable `update` via `Airtable · Update Error`.
- **Doc:** `./Project-C_Visual_Asset_Generation/GHX-05-Social-Asset-Generator/README.md`

## GHX-06-Publish-Queue-Manager
- **Group:** D
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 8 / 9
- **Integrations:** Airtable, Code, IF, Schedule Trigger, Split In Batches
- **AI:** None detected
- **Purpose:** On a schedule, validate ready-to-publish rows and mark publish-ready or append error logs in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Validation Run`). Airtable `search` via `Airtable · Search Ready To Publish`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Validate Publish Gate`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Complete`). Airtable `update` via `Airtable · Mark Publish Ready`. Airtable `update` via `Airtable · Append Error Log`.
- **Doc:** `./Project-D_Commerce_Publish_Etsy/GHX-06-Publish-Queue-Manager/README.md`

## GHX-07-Etsy-Draft-Publisher
- **Group:** D
- **Complexity:** Advanced
- **Status:** Functional Build
- **Nodes / edges:** 18 / 20
- **Integrations:** Airtable, Code, Etsy (via HTTP), HTTP Request, IF, Schedule Trigger, Set, Split In Batches
- **AI:** None detected
- **Purpose:** On a schedule, create Etsy draft listings and upload images/digital files via HTTP, then save results to Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Etsy Draft Run`). Sets fields (`Set · Load Env Config`). Transforms/prepares data in Code node `Code · Setup Config`. Airtable `search` via `Airtable · Search Publish Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Etsy Payload`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Preflight OK`). HTTP request via `HTTP · Etsy Create Draft`. Airtable `update` via `Airtable · Log Etsy Error`. Transforms/prepares data in Code node `Code · Parse Listing Id`. Branches with an IF check (`Filter · Listing Created`). HTTP request via `HTTP · Download Mockup`. HTTP request via `HTTP · Etsy Upload Image`. HTTP request via `HTTP · Download Digital File`. HTTP request via `HTTP · Etsy Upload Digital File`. Transforms/prepares data in Code node `Code · Build Success Payload`. Airtable `update` via `Airtable · Save Etsy Draft`.
- **Doc:** `./Project-D_Commerce_Publish_Etsy/GHX-07-Etsy-Draft-Publisher/README.md`

## GHX-07-Performance-Tracker
- **Group:** G
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 8 / 8
- **Integrations:** Airtable, Code, HTTP Request, OpenAI (via HTTP), Schedule Trigger, Split In Batches
- **AI:** HTTP · OpenAI Chat → OpenAI Chat
- **Purpose:** On a schedule, review published rows, generate notes via OpenAI HTTP, and save metrics in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Weekly Performance`). Airtable `search` via `Airtable · Search Published`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Score Metrics`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Merge AI Notes`. Airtable `update` via `Airtable · Save Metrics`.
- **Doc:** `./Project-G_Performance_Feedback/GHX-07-Performance-Tracker/README.md`

## GHX-08-Metricool-Scheduler
- **Group:** E
- **Complexity:** Advanced
- **Status:** Functional Build
- **Nodes / edges:** 16 / 18
- **Integrations:** Airtable, Code, HTTP Request, IF, Metricool (via HTTP), OpenAI (via HTTP), Schedule Trigger, Set, Split In Batches
- **AI:** HTTP · OpenAI Chat → OpenAI Chat
- **Purpose:** On a schedule, build social posts (OpenAI + Metricool HTTP) and mark scheduled / log errors / save dry-run packs in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Social Schedule Run`). Sets fields (`Set · Load Metricool Config`). Transforms/prepares data in Code node `Code · Setup Config`. Airtable `search` via `Airtable · Search Social Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Caption Body`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Expand Platform Posts`. Branches with an IF check (`Filter · API Enabled`). HTTP request via `HTTP · Metricool Schedule Post`. Airtable `update` via `Airtable · Save Dry Run Post Pack`. Transforms/prepares data in Code node `Code · Aggregate Schedule Results`. Branches with an IF check (`Filter · Schedule OK`). Airtable `update` via `Airtable · Mark Scheduled`. Airtable `update` via `Airtable · Log Schedule Error`.
- **Doc:** `./Project-E_Social_Scheduling_Metricool/GHX-08-Metricool-Scheduler/README.md`

## GHX-09-Ready-To-Post-Queue
- **Group:** E
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 11 / 12
- **Integrations:** Airtable, Code, IF, Schedule Trigger, Split In Batches
- **AI:** None detected
- **Purpose:** On a schedule, find scheduled content and create ready-to-post queue rows in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Every Hour`). Transforms/prepares data in Code node `Code · Reset Run Counters`. Airtable `search` via `Airtable · Search Scheduled Content`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Ready-To-Post Queue Items`. Transforms/prepares data in Code node `Code · Run Summary`. Branches with an IF check (`Filter · Queue Item OK`). Airtable `create` via `Airtable · Create Ready To Post Row`. Transforms/prepares data in Code node `Code · Log Skipped Item`. Airtable `update` via `Airtable · Mark Queued To Post`. Transforms/prepares data in Code node `Code · Log Queued Item`.
- **Doc:** `./Project-E_Social_Scheduling_Metricool/GHX-09-Ready-To-Post-Queue/README.md`

## GHX-09-Self-Healing-QA
- **Group:** H
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 11 / 13
- **Integrations:** Airtable, Code, HTTP Request, IF, NoOp, Schedule Trigger, Split In Batches
- **AI:** None detected
- **Purpose:** On a schedule, find failed rows and requeue for retry or flag for manual review in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · QA Sweep`). Airtable `search` via `Airtable · Search Failed Rows`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Classify Failure`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Can Auto Retry`). Airtable `update` via `Airtable · Requeue For Retry`. Airtable `update` via `Airtable · Flag Manual Review`. Branches with an IF check (`Filter · Webhook Set`). HTTP request via `HTTP · Admin Alert`. No-op placeholder (`No Op · Skip Alert`).
- **Doc:** `./Project-H_Reliability_and_Alerts/GHX-09-Self-Healing-QA/README.md`

## GHX-10-Performance-Tracker
- **Group:** G
- **Complexity:** Advanced
- **Status:** Functional Build
- **Nodes / edges:** 12 / 13
- **Integrations:** Airtable, Code, Etsy (via HTTP), HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Split In Batches
- **AI:** HTTP · OpenAI Notes → OpenAI Chat
- **Purpose:** On a schedule, fetch live product metrics (Etsy HTTP + OpenAI notes) and save metrics in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Weekly Metrics`). Airtable `search` via `Airtable · Search Live Products`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Prep Metrics Context`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Has Etsy Listing`). HTTP request via `HTTP · Etsy Get Listing`. Transforms/prepares data in Code node `Code · Score Without Etsy`. Transforms/prepares data in Code node `Code · Score Metrics`. HTTP request via `HTTP · OpenAI Notes` (OpenAI Chat). Transforms/prepares data in Code node `Code · Merge AI Notes`. Airtable `update` via `Airtable · Save Metrics`.
- **Doc:** `./Project-G_Performance_Feedback/GHX-10-Performance-Tracker/README.md`

## GHX-11-Winning-Idea-Loop
- **Group:** A
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 9 / 8
- **Integrations:** Airtable, Code, HTTP Request, IF, NoOp, OpenAI (via HTTP), Schedule Trigger
- **AI:** HTTP · OpenAI Ideas → OpenAI Chat
- **Purpose:** On a schedule, read top-performing rows, generate new ideas via OpenAI HTTP, and create idea rows in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Weekly Idea Loop`). Airtable `search` via `Airtable · Search Top Winners`. Transforms/prepares data in Code node `Code · Build Winner Analysis`. Branches with an IF check (`Filter · Has Winners`). HTTP request via `HTTP · OpenAI Ideas` (OpenAI Chat). No-op placeholder (`No Op · No Winners`). Transforms/prepares data in Code node `Code · Parse New Ideas`. Airtable `create` via `Airtable · Create Idea Rows`. Transforms/prepares data in Code node `Code · Run Complete`.
- **Doc:** `./Project-A_Idea_Intelligence/GHX-11-Winning-Idea-Loop/README.md`

## GHX-12-Content-Idea-Generator
- **Group:** A
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 12 / 13
- **Integrations:** Airtable, Code, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Set, Split In Batches
- **AI:** HTTP · OpenAI Chat → OpenAI Chat
- **Purpose:** On a schedule, find promotable products, generate content ideas via OpenAI HTTP, and create content rows in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Daily Content Ideas`). Sets fields (`Set · Load Content Niches`). Transforms/prepares data in Code node `Code · Setup Config`. Airtable `search` via `Airtable · Search Promotable Products`. Transforms/prepares data in Code node `Code · Build Daily Ideas Body`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Parse Content Ideas`. Processes records in batches (`Batch · Split Ideas`). Branches with an IF check (`Filter · Idea OK`). Transforms/prepares data in Code node `Code · Run Complete`. Airtable `create` via `Airtable · Create Content Row`. Transforms/prepares data in Code node `Code · Log Skip`.
- **Doc:** `./Project-A_Idea_Intelligence/GHX-12-Content-Idea-Generator/README.md`

## GHX-13-Video-Script-Builder
- **Group:** F
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 10 / 11
- **Integrations:** Airtable, Code, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Split In Batches
- **AI:** HTTP · OpenAI Chat → OpenAI Chat
- **Purpose:** On a schedule, generate video scripts via OpenAI HTTP for queued rows and save scripts or errors in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Script Build Run`). Airtable `search` via `Airtable · Search Script Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Script Body`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Parse Platform Scripts`. Branches with an IF check (`Filter · Script OK`). Airtable `update` via `Airtable · Save Scripts`. Airtable `update` via `Airtable · Log Script Error`.
- **Doc:** `./Project-F_Video_Pipeline_HeyGen/GHX-13-Video-Script-Builder/README.md`

## GHX-14-Metricool-Content-Scheduler
- **Group:** E
- **Complexity:** Advanced
- **Status:** Functional Build
- **Nodes / edges:** 16 / 19
- **Integrations:** Airtable, Code, HTTP Request, IF, Metricool (via HTTP), OpenAI (via HTTP), Schedule Trigger, Set, Split In Batches
- **AI:** HTTP · OpenAI Chat → OpenAI Chat
- **Purpose:** On a schedule, process content queue rows, schedule via Metricool HTTP, and save post packs or errors in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Metricool Content Run`). Sets fields (`Set · Load Metricool Config`). Transforms/prepares data in Code node `Code · Setup Config`. Airtable `search` via `Airtable · Search Content Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Metricool Pack Body`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Expand Metricool Posts`. Branches with an IF check (`Filter · Pack OK`). Branches with an IF check (`Filter · API Enabled`). Airtable `update` via `Airtable · Log Scheduler Error`. HTTP request via `HTTP · Metricool Schedule Post`. Airtable `update` via `Airtable · Save Post Pack`. Transforms/prepares data in Code node `Code · Aggregate Metricool Results`. Branches with an IF check (`Filter · Schedule OK`).
- **Doc:** `./Project-E_Social_Scheduling_Metricool/GHX-14-Metricool-Content-Scheduler/README.md`

## GHX-15-Content-QA
- **Group:** F
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 8 / 9
- **Integrations:** Airtable, Code, IF, Schedule Trigger, Split In Batches
- **AI:** None detected
- **Purpose:** On a schedule, review QA queue rows and mark video-ready or needs-fix in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Content QA Sweep`). Airtable `search` via `Airtable · Search QA Queue`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Validate Content Fields`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Content Complete`). Airtable `update` via `Airtable · Mark Video Ready`. Airtable `update` via `Airtable · Mark Needs Fix`.
- **Doc:** `./Project-F_Video_Pipeline_HeyGen/GHX-15-Content-QA/README.md`

## GHX-16-HeyGen-Video-Generator
- **Group:** F
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 13 / 15
- **Integrations:** Airtable, Code, HTTP Request, HeyGen (via HTTP), IF, Schedule Trigger, Set, Split In Batches
- **AI:** HTTP · HeyGen Create Video → HeyGen
- **Purpose:** On a schedule, create HeyGen videos for video-ready rows and mark processing or log errors in Airtable.
- **Plain English:** Starts on a schedule (`Schedule · Every 15 Minutes`). Sets fields (`Set · Load HeyGen Config`). Transforms/prepares data in Code node `Code · Setup Config`. Airtable `search` via `Airtable · Search Video Ready`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build HeyGen Payload`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Payload OK`). HTTP request via `HTTP · HeyGen Create Video` (HeyGen). Airtable `update` via `Airtable · Log HeyGen Error`. Transforms/prepares data in Code node `Code · Parse HeyGen Response`. Branches with an IF check (`Filter · Video Id Returned`). Airtable `update` via `Airtable · Mark Video Processing`.
- **Doc:** `./Project-F_Video_Pipeline_HeyGen/GHX-16-HeyGen-Video-Generator/README.md`

## GHX-17-HeyGen-Status-Poller
- **Group:** F
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 14 / 18
- **Integrations:** Airtable, Code, HTTP Request, HeyGen (via HTTP), IF, Schedule Trigger, Split In Batches, Switch
- **AI:** HTTP · HeyGen Get Status → HeyGen
- **Purpose:** On a schedule, poll HeyGen status for processing videos and update Airtable ready/failed/error fields.
- **Plain English:** Starts on a schedule (`Schedule · Every 10 Minutes`). Airtable `search` via `Airtable · Search Processing Videos`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Prepare Poll Context`. Transforms/prepares data in Code node `Code · Batch Complete`. Branches with an IF check (`Filter · Context OK`). HTTP request via `HTTP · HeyGen Get Status` (HeyGen). Airtable `update` via `Airtable · Log Context Error`. Transforms/prepares data in Code node `Code · Parse HeyGen Status`. Routes with a Switch (`Switch · HeyGen Status`). Airtable `update` via `Airtable · Mark Ready To Schedule`. Transforms/prepares data in Code node `Code · Log Still Processing`. Airtable `update` via `Airtable · Mark Video Failed`. Airtable `update` via `Airtable · Log Poll Error`.
- **Doc:** `./Project-F_Video_Pipeline_HeyGen/GHX-17-HeyGen-Status-Poller/README.md`

## GHX-Generate-Product-Listing
- **Group:** B
- **Complexity:** Intermediate
- **Status:** Functional Build
- **Nodes / edges:** 10 / 11
- **Integrations:** Airtable, Code, HTTP Request, IF, OpenAI (via HTTP), Schedule Trigger, Split In Batches
- **AI:** HTTP · OpenAI Chat → OpenAI Chat
- **Purpose:** On a schedule, search idea records, generate listing JSON via OpenAI HTTP, and update Airtable success/error fields.
- **Plain English:** Starts on a schedule (`Schedule · Listing Run`). Airtable `search` via `Airtable · Search Ideas`. Processes records in batches (`Batch · Split Records`). Transforms/prepares data in Code node `Code · Build Chat Payload`. Transforms/prepares data in Code node `Code · Batch Complete`. HTTP request via `HTTP · OpenAI Chat` (OpenAI Chat). Transforms/prepares data in Code node `Code · Parse Listing JSON`. Branches with an IF check (`Filter · Parse OK`). Airtable `update` via `Airtable · Update Success`. Airtable `update` via `Airtable · Update Error`.
- **Doc:** `./Project-B_Listing_and_Prompt_Generation/GHX-Generate-Product-Listing/README.md`
