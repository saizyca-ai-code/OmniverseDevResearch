---
id: OVR-ADR-0002
title: PoC 0 — 受限 binary identity 替代證明政策候選
type: decision
status: review
created: 2026-10-17
updated: 2026-10-17
domains: [omniverse-kit, rtx, reproducibility]
repositories:
  - https://github.com/saizyca-ai-code/OmniverseDevResearch
  - https://github.com/saizyca-ai-code/ov_dmx_light_control
tags: [poc0, policy-candidate, binary-identity]
---

# PoC 0 — 受限 binary identity 替代證明政策候選

> **待審政策，尚未接受或生效。** 2026-10-17 human owner僅核准B為受限PoC候選方向、保留A的provenance目標、原則接受L01–L05，要求B八條件及E01–E08不可略過。這不是binary baseline批准、B驗收或任何run簽核。本PR不合併、不更新implementation handoff lock、不執行Kit／RTX；目前full environment Go=blocked、Full Gate0 not-assessed。以下「必須／不得」是提議政策的規範內容，須經實質政策review／接受、publication與implementation採用後才供新驗證使用。

## Context、固定依據與證據

研究起點為`594dbb00328802f295a3cccaf6a6daedd5103c08`；implementation仍鎖定`27ab5add5c62692d47662e32401df860a82136cf`，並以`92abd6c4c4cf819395afaac667794914b71ccda5`的既有證據作輸入。本政策不改寫舊run或舊lock的判定。

- [固定AC-02](https://github.com/saizyca-ai-code/OmniverseDevResearch/blob/27ab5add5c62692d47662e32401df860a82136cf/docs/handoffs/precision-lighting-poc0/POC0-ACCEPTANCE.md)要求critical identity resolved，未明定完整renderer Git SHA（A，source-inspected）。
- [OVR-INV-0004原調查](https://github.com/saizyca-ai-code/OmniverseDevResearch/blob/594dbb00328802f295a3cccaf6a6daedd5103c08/docs/research/OVR-INV-0004-rtx-identity-research-feedback.md)保留A／B比較、SDK／DLL來源鏈、archive差異及bounded search；本ADR是詳細政策唯一位置，不將調查merge當政策接受。
- [baseline report](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/docs/development/pr01-report.md)：歷史USD／RT2／PT各兩次成功；[T005 review JSON](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/docs/development/evidence/t004-review-observed.json)：28個plugin path/hash吻合、11 checks、build全dev。這些是歷史直接runtime證據（A），不是B-pass。
- [resolution lock](https://github.com/saizyca-ai-code/ov_dmx_light_control/blob/92abd6c4c4cf819395afaac667794914b71ccda5/tools/bootstrap/resolution.lock.json)與review交叉核對（B）：35檔／30DLL／28plugins，非完整SDK／driver SBOM。`187cf21b`是Kit target／publication，`1ea54838`是SDK dependency宣告，兩者不可互換。權威loaded-bytes映射與原archive checksum仍未知（U，not-verified）。Evidence Policy A／B類別與本文件方案A／B不同。

## Decision proposed、alternatives與適用範圍

| 路徑 | 證明目的與必要資料 | 風險／代價 |
|---|---|---|
| A vendor provenance | owner事先指定粒度的唯一vendor build ID或source revision，權威manifest／attestation／可保存vendor映射連到精確packages與關鍵DLL digests，再核對loaded paths／hashes | 只給Kit版本或label不夠，source SHA也不保證compiler／flags／deps相同；權威資料取得時間未知 |
| B restricted binary identity | human核准的確切集合與環境、受控pre／runtime／post、真實行為與獨立human驗收，全部符合B01–B08／E01–E08 | hash不能證明vendor來源、安全或source lineage；需要coverage、checker、保存與重驗成本 |

B只適用可信本機、非惡意漂移及目前一般燈光PoC0 baseline。候選目標是既有Windows11／RTX5080／driver616.92、Kit110.4.0+feature.386251.187cf21b.gl、kernel210.4.11+release.15522.174283e4.gl、embeddedUSD0.25.11／Python3.12.14；仍須新run證明實際環境及核准適用性，不因列在此就批准。driver／OS／GPU／SDK或任一critical輸入改變須impact review及必要重驗。

不涵蓋fresh-host reacquisition、compromised host、memory attestation、vendor authenticity、產品安全、precision projector、AOV語意／物理lux或效能。若用途要求上述任一未被B證明的性質，B不得取代其要求；應回到A或另提方案。PRD的另一開發者重建目標保留，B局部identity接受不證明該目標或完整PoC成功，未完成證據須另列供human Gate review。這不是PR-02啟動授權。

### B八項不可略過條件

| ID | 必須滿足 |
|---|---|
| B01 信任根與coverage | human review取得／授權／package refs／source-config，指定集合與coverage；35檔、四package的28plugins及2 support DLL／metadata只是起點。未知critical或未處置具體integrity疑點阻擋。run前必須批准指定集合，agent不能批准自己 |
| B02 可重算集合識別 | 固定versioned schema、raw-byte SHA256、canonical規則／test vectors；binary集合ID與環境ID分開並互引，不用commit或archive名稱假扮digest |
| B03 綁定執行與漂移控制 | 完整核准集合pre／clean exit後post，run內documented loaded paths/hash／確切plugin set／versions／enabled metadata及pre-post source fingerprints；禁止in-place更新。missing／extra／duplicate／unknown／mismatch不得pass，缺必要輸出阻擋B。pre/post相同也不能排除惡意替換後還原、未涵蓋modules或記憶體修改，故僅限可信本機非惡意漂移 |
| B04 行為證據 | 固定實際OS／GPU／driver／Kit／kernel／USD／Python／scene／settings／sampling／denoising／曝光／完整命令，USD roundtrip與RT2／PT各兩次；CI不能代GPU |
| B05 誠實unknown | internal revision仍null／unavailable及missing reason，identity_method明標binary身份，不把dev或Kit hash填為唯一RTX revision；舊run不改寫 |
| B06 限定用途與變更 | 只對已批准files、環境及scope有效；critical binary／module set變更需新集合批准，環境變更須impact review。不可改lock或重算manifest來消除mismatch |
| B07 留存與復原 | 具名custodian、授權範圍內保管與可檢視／可恢復證據；不暗中複製或散布binary。bytes或證據遺失停止將歷史接受用於新run；fresh-host若為硬需求則現有B不足 |
| B08 human鏈 | 方向／政策接受、run前集合批准、run後獨立於coding agent的human結果接受分開；同一human可多角色但逐項記錄。不能用籠統風險接受豁免最低條件；補測未授權則保留gap |

### L01–L05：原則接受與不可豁免界線

| ID | 受限用途可原則承擔的未知 | 不可推導／豁免 |
|---|---|---|
| L01 | internal revision unavailable、28plugins dev | 不證明vendor認證或安全，不偽造revision／hash等價 |
| L02 | 原ZIP bytes／checksum未取得及folder hash差異的來源不確定性 | E01須列疑點、證據、替代解釋、處置或僅殘留未知的理由及human review；原因未證明不稱已解。owner承擔風險不是處置證據，具體疑點未處置仍blocked |
| L03 | 非完整SDK／driver SBOM，非memory attestation，只限可信本機 | 先判criticality再記涵蓋或排除；unknown／未涵蓋critical不能用excluded標籤豁免 |
| L04 | fresh-host尚未證明，僅評估保存集合的本機重跑 | E07及其餘條件仍須完成；不宣稱B流程或復原已驗證，遺失即停止新run沿用 |
| L05 | 固定一般燈光場景、解析度、曝光、denoiser／color pipeline下的baseline | 無跨環境、projector、AOV、lux、效能或產品保證；不授權PR-02 |

原archive搜尋只涵蓋repository內三個cache roots，未查system temporary／external-global caches。folder hash差異不是integrity pass或已證實corruption。缺vendor證據不證明無疑點；L原則接受不等於指定集合的E01通過。

## Coverage、criticality與證據最低要求

Coverage record必須是受版本管理的獨立evidence，以其raw-byte SHA256綁到run前批准。每項記：stable item ID、package/ref、觀察來源、criticality、用途／理由、涵蓋方式與evidence refs、未涵蓋風險、reviewer及決定。批准者必須可取得與核對相關raw evidence，公開摘要hash本身不提供bytes。

1. 會影響Kit啟動、已用RTX plugin／dependency、USD讀寫、renderer mode、測試控制或結果判定者為critical；已知35檔及28plugins不能自動縮減。實際關鍵輸入、runtime發現新module及其依賴須評估，不聲稱已列舉全機transitive modules。
2. 先判criticality，再選`binary`（入集合）、`environment`（環境冊證據）或`excluded`（受限目標不需要且有理由）涵蓋方式。critical不是excluded的反義分類；未知criticality或未充分涵蓋critical不得排除／pass。
3. 用於run的critical SDK／RTX files、app／probe／executor來源及scene/settings均須固定hash。前者入binary manifest，後者由環境record引用其raw source／input snapshot hashes。runtime plugin inventory須精確比對核准28集合或另經review的完整新集合，不能只檢查subset。
4. OS／GPU／driver可用環境冊記錄實際build／model／driver版本、API、取得方式與時間及比對結果；不因此認證driver bytes。只有human明確接受此方法足以涵蓋可信本機的行為風險時才可用。若需求包括driver byte integrity、證據不可得或實際環境不符，保持blocked，不強行排除。
5. Run前批准必須包含collection roots／scan domains、exact covered set、預期plugin set及排除catalog。pre/post核對整個covered set，掃描domains內未列入covered或已review排除catalog的extra須阻擋；域外與未觀察依賴仍須如實列限制，不能聲稱完整SBOM。新unknown runtime module須另行診斷／review，不在該未批准run直接給B-pass。

## Canonical identity contract v1（提案，待實作）

### Binary集合payload與ID

Payload恰含`schema`與`files`：schema=`poc0-binary-set/1`，files為非空array。entry恰含`root`、`path`、`size_bytes`、`sha256`；root只可`kit`或`registry`，對應本機核准absolute roots，root mapping另記在批准證據，不上傳personal path。path為相對root的canonical logical path，不能把本機cache完整路徑寫入ID。

- path只允許lowercase ASCII `[a-z0-9._/-]`；不得absolute、drive／UNC／colon、backslash、空component、`.`／`..`、尾斜線、Windows尾點／尾空白component或DOS device components。DOS拒絕規則為component第一個dot前的lowercase部分等於`con`、`prn`、`aux`、`nul`或符合`com[1-9]`／`lpt[1-9]`（因此nul.txt亦拒絕）。root／path pair唯一，所有entry按ASCII `(root,path)`排序。先驗證實際path唯一且位於核准root，再將separator轉`/`及ASCII大寫轉小寫；case-fold collision、duplicate、symbolic link／junction／reparse point（root及沿途component亦同）、未存在／不可讀或越界一律拒絕，不能靠去掉`..`消歧。
- size_bytes為0至9007199254740991的JSON integer，禁止bool／float，來源是實際raw bytes長度；sha256為raw bytes SHA256的64位lowercase hex。無newline文字正規化、無截短、無vendor folder-hash替代。
- canonical bytes為ASCII編碼的JSON，object keys lexicographic排序、無縮排或分隔空白、最後恰一個LF，無BOM。printable ASCII字串僅double quote與backslash分別用JSON反斜線escaping，其餘字元逐字輸出，不使用slash或Unicode escape。key集合固定，沒有null／float／NaN；parsed輸入中的duplicate JSON object keys也須拒絕，不能先讓parser覆蓋後再檢查。必須從parsed有效payload重算canonical bytes，不hash任意pretty JSON檔案。
- `binary_set_id = "sha256:" + SHA256(canonical bytes).hexdigest()`。ID不是payload欄位；approval、run ID、timestamps、環境資料、evidence檔案及自身ID均不在payload，避免自我引用。更換file／size／digest／logical path必然要求重算與新批准，不可藉重新生成ID把漂移當既有pass。

### 環境payload、環境ID與綁定

環境payload恰含`schema`=`poc0-run-environment/1`及`values`（object）。values keys須lowercase ASCII snake_case，values須非空printable ASCII strings（0x20–0x7e，禁止control與non-ASCII）；保留原值不trim或case-fold。這是canonical描述契約，不限制私人raw evidence的encoding；本機localized資料須另存raw並明列其可核對ASCII描述方法。

Required keys：`windows_build`、`gpu_model`、`driver_version`、`graphics_api`、`kit_build`、`kernel_build`、`embedded_openusd`、`embedded_python`、`renderer_mode`、`implementation_commit`、`source_snapshot_sha256`、`scene_sha256`、`settings_sha256`、`command_spec_sha256`。implementation_commit須40位lowercase hex；所有`*_sha256`值須64位lowercase hex、且對應實際raw artifact。source snapshot須列所有app／probe／executor來源的path／hash，前後核對；command spec須含可審的normalized argv／cwd mapping／flags與重要env。必要版本或輸入未知不得用占位字串通過。可加額外同型keys，新增值會改變環境ID。

canonical序列化同上；`environment_id = "sha256:" + SHA256(canonical bytes).hexdigest()`。renderer_mode逐run實際記錄，USD-only時明列`usd-only`，不能由檔名推論mode。binary_set_id不放入環境payload，兩ID在run envelope與run前approval互引，因此無digest循環。批准可列有限的per-mode environment IDs（USD、RT2、PT）及對應命令；任何未批准的mode／settings／來源或環境改變不得沿用。

### Run envelope與人類批准契約

Schema example0.2中的`identity`為主record：policy ID／採用的實際merged研究SHA、method=`vendor-provenance|binary-identity`或未選時null、declared build、internal revision／missing reason、binary／environment payload refs及IDs、coverage SHA、pre/runtime/post證據refs、E項結果與human批准refs。範例欄位是null時不代表滿足required runtime值；schema shape valid不等於驗收pass。

每個evidence ref為相對evidence root的path與raw-byte SHA256；禁止absolute／`..`、秘密與私人raw log上傳。內部evidence可在授權範圍檢視，公開摘要只發清理後path／hash；evidence artifact不hash包含自身hash的record。run envelope與批准record以stable IDs互引；可在外部index記envelope hash，不在envelope內要求自己的hash。

Run前human approval至少記：approval ID、actor（具名human角色）、UTC時間、policy ID／merged SHA、binary_set_id、允許environment IDs、coverage record SHA、信任根review／E01與E07 refs、L逐項接受與未解gap、受控執行安排、scope及execution authorization reference。不得在存在未處置critical gap時批准B候選驗收run。沒有批准的新module探索只能另經授權作diagnostic，不得追認為B驗收。

Run後human review另記：review ID、actor、UTC時間、run IDs與run前approval ID、被審查的envelope／證據hashes、E01–E07逐項結果、限制、decision=`accept|reject`及理由。human必須獨立於執行coding agent，同一maintainer可多human角色但記錄分開。run後接受不批准新baseline，不以預先存在B-pass為接受前提。候選驗收前／後human record皆須有`actor_kind=human`及可審查的真人授權依據，不是只靠自填actor字串通過。各E execution status沿用pass／fail／blocked／not-run；identity_acceptance_status亦同，未簽核時blocked而diagnostic可pass。

### 正例／負例規格

Canonical test vectors為**合成資料，不是SDK檔案或approved baseline**。implementation須在ordinary Python／CI驗證兩平台可得到相同canonical bytes／ID；不因此宣稱Kit可跨平台執行。固定vector與其expected digest見下方generated block；生成程式不隨本政策發布為產品checker。

<!-- CANONICAL-VECTORS-BEGIN -->
```json
[
  {
    "name": "synthetic-binary",
    "payload": {
      "schema": "poc0-binary-set/1",
      "files": [
        {
          "root": "kit",
          "path": "b.txt",
          "size_bytes": 2,
          "sha256": "73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac"
        },
        {
          "root": "registry",
          "path": "a.txt",
          "size_bytes": 0,
          "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }
      ]
    },
    "canonical_ascii": "{\"files\":[{\"path\":\"b.txt\",\"root\":\"kit\",\"sha256\":\"73cb3858a687a8494ca3323053016282f3dad39d42cf62ca4e79dda2aac7d9ac\",\"size_bytes\":2},{\"path\":\"a.txt\",\"root\":\"registry\",\"sha256\":\"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\",\"size_bytes\":0}],\"schema\":\"poc0-binary-set/1\"}\n",
    "expected_id": "sha256:eb6eae6e71cd4622fab0af9aa4121ba2ece02ea99813015924fbf48818a5a539"
  },
  {
    "name": "synthetic-environment",
    "payload": {
      "schema": "poc0-run-environment/1",
      "values": {
        "windows_build": "synthetic-windows",
        "gpu_model": "synthetic-gpu",
        "driver_version": "synthetic-driver",
        "graphics_api": "synthetic-api",
        "kit_build": "synthetic-kit",
        "kernel_build": "synthetic-kernel",
        "embedded_openusd": "synthetic-usd",
        "embedded_python": "synthetic-python",
        "renderer_mode": "usd-only",
        "implementation_commit": "0000000000000000000000000000000000000000",
        "source_snapshot_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
        "scene_sha256": "1111111111111111111111111111111111111111111111111111111111111111",
        "settings_sha256": "2222222222222222222222222222222222222222222222222222222222222222",
        "command_spec_sha256": "3333333333333333333333333333333333333333333333333333333333333333"
      }
    },
    "canonical_ascii": "{\"schema\":\"poc0-run-environment/1\",\"values\":{\"command_spec_sha256\":\"3333333333333333333333333333333333333333333333333333333333333333\",\"driver_version\":\"synthetic-driver\",\"embedded_openusd\":\"synthetic-usd\",\"embedded_python\":\"synthetic-python\",\"gpu_model\":\"synthetic-gpu\",\"graphics_api\":\"synthetic-api\",\"implementation_commit\":\"0000000000000000000000000000000000000000\",\"kernel_build\":\"synthetic-kernel\",\"kit_build\":\"synthetic-kit\",\"renderer_mode\":\"usd-only\",\"scene_sha256\":\"1111111111111111111111111111111111111111111111111111111111111111\",\"settings_sha256\":\"2222222222222222222222222222222222222222222222222222222222222222\",\"source_snapshot_sha256\":\"0000000000000000000000000000000000000000000000000000000000000000\",\"windows_build\":\"synthetic-windows\"}}\n",
    "expected_id": "sha256:6c96d4191c0b0bfe71c17a21ac2f5d822a9b2c7b54744615d8160a51f7cb34ee"
  }
]
```
<!-- CANONICAL-VECTORS-END -->

必要負例：empty file set；unknown／missing keys；noninteger／bool size；bad／uppercase／truncated digest；duplicate與case collision；unsorted canonical entry input須先排序再serialize；absolute／UNC／drive／`..`／空component／尾點／link／越界／不可讀file；raw bytes與metadata不符；missing／extra runtime plugin、duplicate name/path、hash mismatch；pre/post不同、source／env漂移、missing post、timeout／bad exit；unknown critical；錯policy SHA、缺run前批准／coverage／custodian、冒用agent為human、run後批准套錯ID、沒有E08結果。所有負例不得導出B-pass；正常diagnostic assertions可獨立於human結果判定。

## E01–E08必補證據與無循環取得程序

| ID | 必補證據；目前均未完成 |
|---|---|
| E01 | 取得／授權／package／config及疑點清單、證據與替代解釋、處置或僅殘留未知的理由、具名human review；無未處置具體integrity疑點。缺vendor資訊不證明無疑點，L原則接受不證明本項通過 |
| E02 | coverage record及criticality／涵蓋方法／排除／未涵蓋風險／review；binary或環境證據未充分涵蓋critical、未分類unknown須解決或blocked |
| E03 | 本契約的schema／ID／canonical規則與合成vectors正負例、實際manifest及環境互引；不能以目前lock當完整集合ID |
| E04 | 同run完整pre／runtime／clean exit後post、源指紋、plugin／版本及控制安排／負例，缺輸出或漂移不得B-pass |
| E05 | 政策發布／implementation採用與指定集合run前批准後，USD／RT2／PT各兩次，完整命令／環境／scene／settings／timestamps／exit／assertions／hashes；歷史六次只供對照 |
| E06 | diagnostic結果、B最終identity驗收、full environment Go及Gate0分層，錯誤及負例；checker不自簽human，也不為等human而將實際成功diagnostic偽報失敗 |
| E07 | 具名custodian、evidence／manifest可恢復確認、cache保管／停止清理與授權檢視安排，丟失時停止沿用；不暗中複製SDK或宣稱fresh-host重建 |
| E08 | 方向與L決定、實質政策review／publication／實際merged SHA、adoption PR／impact note；run前子項批准指定集合／環境／coverage／限制，run後子項由human審查實際E01–E07接受或拒絕。兩子項分開，不能追認未批准baseline |

1. S1：owner方向／條件框架已核准；詳細政策仍待review，具名baseline批准者／custodian／reviewer仍未指定。
2. S2：本獨立研究PR review；只有另行明確的政策接受及merge後，才取得實際merged政策SHA。status review或PR建立本身不生效。本次禁止merge。
3. S3：另經授權、review的implementation adoption PR以該SHA更新lock、impact note及所需schema／checker／負例；採用政策不代表B驗收，Go仍blocked。
4. S4-run前：E01／E02／E03／E07準備及E04／E06 checker負例／控制安排已審，E08 run前子項批准指定集合／有限環境IDs；另有明確execution授權才可run。
5. S4-run後：執行E04／E05、產出E06待審結果、獨立human完成E08 run後接受／拒絕，才評估B最終identity驗收。E04 post／E05／E08 run後結果無須先於S3存在。不能以B-pass作human簽核先決條件。

任何必要gap未完成，B最終驗收不得pass。已執行assertion不符合是fail；依賴／環境不可用是blocked；未嘗試是not-run；保持原失敗並以新run重試。取得A或完成B最多解除identity一項，不自動符合其他AC或Full Gate0；Conditional Go原Pure Core限制不變，本次也未授予Conditional Go／PR-02。

## Compatibility、採用與重審

Example schema0.1仍是歷史格式；0.2是本候選新增identity分層契約。讀取0.1可作legacy inventory／歷史診斷，不含B證據就不能推斷B-pass。0.1→0.2不是給舊run補預設approved／pass的自動migration；現有implementation不改格式／assessor，待獨立adoption PR處理。example的歷史research_baseline不是policy merged SHA，也不是implementation lock。

Binary或plugin set、OS／driver／GPU／embedded runtime、scene／settings／source／command任何critical改變，或source信任問題、cache／證據遺失、owner撤回L接受、新官方mapping出現，均須impact review與必要新集合／批准／重驗。保存舊結論適用的政策與evidence，不改hash讓mismatch消失，不自動改lock或Git回退。A不必作為B未來都要取得的vendor資料補件，但用途若要求provenance則B不能豁免A。

## Validation與角色分工

本PR只有政策文件／example／生成索引，沒有runtime執行、產品checker或test probe實作。研究metadata／index／pytest／JSON及合成vector checks的實際結果列PR描述；全部不證明SDK／GPU或B已驗收。

Chat研究端可完成API／規格／政策／驗證計畫與human決策；Codex在獨立明確授權的implementation repo撰寫probe、執行Kit／RTX與交付證據，研究端再review／回寫發現。PR-02 T05–T07是實作及實測交付，不是只讀文件的研究；本ADR不啟動它。
