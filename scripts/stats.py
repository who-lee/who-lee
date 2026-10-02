#!/usr/bin/env python3
"""Builds stats.svg (big contribution count + heatmap) from the GitHub GraphQL API.
Env: GITHUB_TOKEN, LOGIN. Output: dist/stats.svg"""
import os, json, datetime as dt, urllib.request

LOGIN = os.environ["LOGIN"]
TOKEN = os.environ["GITHUB_TOKEN"]
INK, RED, AMB, BLU, CRM = "#17181B", "#E4572E", "#E8962C", "#2743F0", "#F6EEDD"
GLYPHS = json.loads(r'''{"upem":1000,"g":{"0":["M534.5 -15.0Q376.0 -15.0 270.5 11.0Q165.0 37.0 112.5 94.0Q60.0 151.0 60.0 244.0Q60.0 337.0 112.5 394.5Q165.0 452.0 270.5 478.5Q376.0 505.0 534.5 505.0Q693.0 505.0 797.5 478.5Q902.0 452.0 954.0 394.5Q1006.0 337.0 1006.0 244.0Q1006.0 151.0 954.0 94.0Q902.0 37.0 797.5 11.0Q693.0 -15.0 534.5 -15.0ZM534.5 135.0Q609.0 135.0 659.0 147.5Q709.0 160.0 735.0 184.0Q761.0 208.0 761.0 244.0Q761.0 280.0 735.5 304.5Q710.0 329.0 660.0 342.0Q610.0 355.0 535.5 355.0Q461.0 355.0 409.5 342.5Q358.0 330.0 331.5 304.86431884765625Q305.0 279.7286376953125 305.0 243.5577850341797Q305.0 208.0 331.0 184.0Q357.0 160.0 408.5 147.5Q460.0 135.0 534.5 135.0Z",1066],"1":["M25.0 300.0V490.0H459.0V0.0H219.0V300.0H25.0Z",529],"2":["M503.0 150.0 286.0 122.0 285.0 132.0 962.0 155.0V0.0H72.0V125.0Q231.0 153.0 351.0 175.5Q471.0 198.0 550.5 217.5Q630.0 237.0 670.0 256.5Q710.0 276.0 710.0 299.0Q710.0 315.0 693.0 322.5Q676.0 330.0 631.5 333.0Q587.0 336.0 504.0 336.0Q398.0 336.0 344.0 319.5Q290.0 303.0 285.0 268.0H35.0Q35.0 342.0 89.0 395.0Q143.0 448.0 249.5 476.5Q356.0 505.0 513.0 505.0Q606.0 505.0 687.5 497.5Q769.0 490.0 831.0 471.0Q893.0 452.0 928.0 418.5Q963.0 385.0 963.0 333.0Q963.0 287.0 929.0 257.0Q895.0 227.0 833.0 208.0Q771.0 189.0 687.0 176.0Q603.0 163.0 503.0 150.0Z",1003],"3":["M582.0 171.0 580.0 176.0Q676.0 176.0 756.5 172.0Q837.0 168.0 896.0 154.0Q955.0 140.0 987.5 110.0Q1020.0 80.0 1020.0 27.0Q1020.0 -39.0 959.5 -83.0Q899.0 -127.0 787.0 -149.0Q675.0 -171.0 521.0 -171.0Q365.0 -171.0 256.5 -142.5Q148.0 -114.0 91.5 -59.0Q35.0 -4.0 35.0 77.0H286.0Q288.0 55.0 319.5 42.5Q351.0 30.0 404.0 24.5Q457.0 19.0 521.0 19.0Q640.0 19.0 697.5 28.5Q755.0 38.0 755.0 77.0Q755.0 115.0 685.0 124.0Q615.0 133.0 480.0 133.0H331.0V203.0H480.0Q579.0 203.0 636.0 208.5Q693.0 214.0 716.5 227.5Q740.0 241.0 740.0 263.0Q740.0 295.0 688.5 307.5Q637.0 320.0 526.0 320.0Q420.0 320.0 355.5 302.5Q291.0 285.0 287.0 252.0H38.0Q38.0 319.0 76.0 368.0Q114.0 417.0 181.5 448.5Q249.0 480.0 337.5 495.0Q426.0 510.0 526.0 510.0Q678.0 510.0 783.5 490.5Q889.0 471.0 944.5 432.0Q1000.0 393.0 1000.0 333.0Q1000.0 284.0 969.0 253.0Q938.0 222.0 882.0 204.5Q826.0 187.0 749.5 180.0Q673.0 173.0 582.0 171.0Z",1055],"4":["M900.0 495.0V-145.0H660.0V391.0L751.0 341.0L308.0 57.0L291.0 115.0H676.0V-35.0H50.0V115.0L660.0 495.0H900.0ZM884.0 -35.0V115.0H1064.0V-35.0H884.0Z",1094],"5":["M650.0 236.0Q712.0 236.0 768.5 227.5Q825.0 219.0 869.0 198.0Q913.0 177.0 939.0 141.0Q965.0 105.0 965.0 51.0Q965.0 -24.0 916.0 -73.0Q867.0 -122.0 769.5 -146.0Q672.0 -170.0 526.0 -170.0Q431.0 -170.0 346.0 -155.5Q261.0 -141.0 195.5 -112.5Q130.0 -84.0 92.5 -44.0Q55.0 -4.0 55.0 47.0H275.0Q278.0 33.0 312.0 22.0Q346.0 11.0 398.5 5.5Q451.0 0.0 509.0 0.0Q547.0 0.0 585.5 1.0Q624.0 2.0 655.5 7.0Q687.0 12.0 706.0 23.0Q725.0 34.0 725.0 54.0Q725.0 75.0 705.5 86.5Q686.0 98.0 654.0 103.0Q622.0 108.0 584.0 109.0Q546.0 110.0 509.0 110.0Q464.0 110.0 416.0 106.5Q368.0 103.0 329.5 98.5Q291.0 94.0 272.0 89.0L74.0 124.0L124.0 500.0H883.0V310.0H340.0L316.0 134.0L284.0 138.0Q310.0 162.0 366.0 184.5Q422.0 207.0 496.0 221.5Q570.0 236.0 650.0 236.0Z",1015],"6":["M692.0 440.0Q826.0 440.0 916.5 411.0Q1007.0 382.0 1052.5 331.0Q1098.0 280.0 1098.0 214.0Q1098.0 148.0 1047.0 95.0Q996.0 42.0 888.0 11.0Q780.0 -20.0 610.0 -20.0Q420.0 -20.0 291.0 4.0Q162.0 28.0 96.0 77.0Q30.0 126.0 30.0 202.0Q30.0 226.0 41.5 258.0Q53.0 290.0 92.0 325.0Q97.0 330.0 120.5 349.5Q144.0 369.0 179.0 397.5Q214.0 426.0 254.0 459.0Q294.0 492.0 333.0 524.0Q372.0 556.0 404.5 582.0Q437.0 608.0 456.5 624.0Q476.0 640.0 476.0 640.0H814.0L180.0 202.0L117.0 152.0Q195.0 222.0 260.5 276.0Q326.0 330.0 390.5 366.5Q455.0 403.0 527.5 421.5Q600.0 440.0 692.0 440.0ZM588.0 151.0Q714.0 151.0 781.0 167.0Q848.0 183.0 848.0 219.0Q848.0 252.0 781.0 271.0Q714.0 290.0 588.0 290.0Q446.0 290.0 363.0 271.0Q280.0 252.0 280.0 219.0Q280.0 183.0 363.0 167.0Q446.0 151.0 588.0 151.0Z",1133],"7":["M60.0 300.0V490.0H1073.0V300.0L568.0 -150.0H241.0L834.0 371.0L861.0 300.0H60.0Z",1153],"8":["M540.0 339.0Q366.0 339.0 261.5 352.5Q157.0 366.0 110.5 398.0Q64.0 430.0 64.0 484.0Q64.0 539.0 110.5 578.0Q157.0 617.0 261.5 638.5Q366.0 660.0 540.0 660.0Q715.0 660.0 819.5 638.5Q924.0 617.0 970.5 578.0Q1017.0 539.0 1017.0 484.0Q1017.0 430.0 970.5 398.0Q924.0 366.0 819.5 352.5Q715.0 339.0 540.0 339.0ZM540.0 379.0Q634.0 379.0 684.0 386.0Q734.0 393.0 753.0 405.0Q772.0 417.0 772.0 432.0Q772.0 447.0 753.0 457.5Q734.0 468.0 684.0 473.0Q634.0 478.0 540.0 478.0Q447.0 478.0 399.5 473.0Q352.0 468.0 335.5 457.5Q319.0 447.0 319.0 432.0Q319.0 417.0 335.5 405.0Q352.0 393.0 399.5 386.0Q447.0 379.0 540.0 379.0ZM540.0 -20.0Q355.0 -20.0 244.0 6.0Q133.0 32.0 84.0 77.0Q35.0 122.0 35.0 178.0Q35.0 247.0 86.5 283.0Q138.0 319.0 249.0 332.0Q360.0 345.0 540.0 345.0Q720.0 345.0 831.5 332.0Q943.0 319.0 994.5 283.0Q1046.0 247.0 1046.0 178.0Q1046.0 122.0 996.5 77.0Q947.0 32.0 836.0 6.0Q725.0 -20.0 540.0 -20.0ZM540.0 169.0Q644.0 169.0 700.5 174.5Q757.0 180.0 779.0 191.5Q801.0 203.0 801.0 220.0Q801.0 237.0 779.0 248.0Q757.0 259.0 700.5 264.5Q644.0 270.0 540.0 270.0Q437.0 270.0 383.0 264.5Q329.0 259.0 309.5 248.0Q290.0 237.0 290.0 220.0Q290.0 203.0 309.5 191.5Q329.0 180.0 383.0 174.5Q437.0 169.0 540.0 169.0Z",1081],"9":["M441.0 60.0Q307.0 60.0 216.5 89.0Q126.0 118.0 80.5 169.0Q35.0 220.0 35.0 286.0Q35.0 358.0 88.0 409.0Q141.0 460.0 257.5 487.5Q374.0 515.0 564.0 515.0Q754.0 515.0 878.0 492.0Q1002.0 469.0 1062.5 421.5Q1123.0 374.0 1123.0 298.0Q1123.0 267.0 1106.0 233.0Q1089.0 199.0 1046.0 160.0Q1042.0 156.0 1020.0 137.0Q998.0 118.0 964.5 90.0Q931.0 62.0 892.0 30.0Q853.0 -2.0 815.0 -34.0Q777.0 -66.0 745.5 -92.0Q714.0 -118.0 695.0 -134.0Q676.0 -150.0 676.0 -150.0H339.0L972.0 298.0L1036.0 338.0Q958.0 272.0 891.0 220.0Q824.0 168.0 756.5 132.5Q689.0 97.0 613.0 78.5Q537.0 60.0 441.0 60.0ZM564.0 350.0Q422.0 350.0 353.5 335.5Q285.0 321.0 285.0 281.0Q285.0 244.0 353.5 227.0Q422.0 210.0 564.0 210.0Q706.0 210.0 789.5 227.0Q873.0 244.0 873.0 281.0Q873.0 308.0 835.0 323.0Q797.0 338.0 728.0 344.0Q659.0 350.0 564.0 350.0Z",1158],",":["M53.0 -167.0 39.0 -105.0Q55.0 -97.0 72.5 -69.5Q90.0 -42.0 93.0 -11.0L25.0 0.0V153.0H278.0V60.0Q278.0 -31.0 225.0 -92.0Q172.0 -153.0 53.0 -167.0Z",303]}}''')
UPEM = GLYPHS["upem"]; G = GLYPHS["g"]

def gql(q):
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": q}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req))
    if "errors" in d: raise SystemExit(d["errors"])
    return d["data"]

now = dt.datetime.now(dt.timezone.utc)
base = gql('{user(login:"%s"){createdAt repositories(ownerAffiliations:OWNER,privacy:PUBLIC,first:100){totalCount nodes{stargazerCount}} contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}' % LOGIN)["user"]
cal = base["contributionsCollection"]["contributionCalendar"]
days = [d for w in cal["weeks"] for d in w["contributionDays"]]
year_total = cal["totalContributions"]

# lifetime = sum of 1-year windows since account creation
created = dt.datetime.fromisoformat(base["createdAt"].replace("Z", "+00:00"))
life, start = 0, created
while start < now:
    end = min(start + dt.timedelta(days=365), now)
    q = '{user(login:"%s"){contributionsCollection(from:"%s",to:"%s"){contributionCalendar{totalContributions}}}}' % (
        LOGIN, start.strftime("%Y-%m-%dT%H:%M:%SZ"), end.strftime("%Y-%m-%dT%H:%M:%SZ"))
    life += gql(q)["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    start = end

# streaks
counts = [d["contributionCount"] for d in days]
longest = run = 0
for c in counts:
    run = run + 1 if c else 0
    longest = max(longest, run)
cur = 0
i = len(counts) - 1
if i >= 0 and counts[i] == 0: i -= 1  # today may still be empty
while i >= 0 and counts[i] > 0:
    cur += 1; i -= 1

repos = base["repositories"]["totalCount"]
stars = sum(n["stargazerCount"] for n in base["repositories"]["nodes"])

def num(text, x, y, size, fill):
    s = size / UPEM; out = []; cx = 0
    for ch in text:
        d, adv = G[ch]
        out.append(f'<g transform="translate({x + cx*s:.2f} {y}) scale({s:.5f} {-s:.5f})"><path d="{d}" fill="{fill}"/></g>')
        cx += adv
    return "".join(out), cx * s

W, H = 880, 322
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{year_total:,} contributions in the last year, {life:,} lifetime">',
     f'<title>{year_total:,} contributions in the last year</title>',
     '<style>.c{animation:p .5s cubic-bezier(.2,.9,.3,1.3) both}@keyframes p{from{opacity:0;transform:scale(.2)}}'
     '.c{transform-box:fill-box;transform-origin:center}.pop{animation:u .6s cubic-bezier(.2,.9,.3,1.25) both}@keyframes u{from{opacity:0;transform:translateY(24px)}}'
     '.l{font:700 12px "Segoe UI",Helvetica,Arial,sans-serif;letter-spacing:1.5px;fill:%s}@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>' % INK,
     f'<rect width="{W}" height="{H}" fill="{CRM}"/>']

# big number with hard shadow
txt = f"{year_total:,}"
sh, _ = num(txt, 37, 133, 84, AMB)
big, bw = num(txt, 32, 128, 84, INK)
o.append('<g class="pop">' + sh + big + '</g>')
o.append(f'<text class="l" x="36" y="36">CONTRIBUTIONS · LAST 12 MONTHS</text>')

# stat chips
best = max(counts) if counts else 0
chips = [(f"{life:,}", "LIFETIME", RED), (f"{cur}", "DAY STREAK", BLU), (f"{longest}", "LONGEST STREAK", AMB), (f"{best}", "BEST DAY", INK)]
for k, (v, label, col) in enumerate(chips):
    gx = 580 + (k % 2) * 160; gy = 52 + (k // 2) * 64
    n, w = num(v, gx, gy + 30, 30, col)
    o.append(f'<g class="pop" style="animation-delay:{0.2+0.1*k:.1f}s">' + n + f'<text class="l" x="{gx}" y="{gy+48}" style="font-size:10px">{label}</text></g>')

# heatmap
vals = sorted(c for c in counts if c)
def q(p): return vals[int(len(vals) * p)] if vals else 1
t1, t2, t3 = q(0.25), q(0.5), q(0.75)
pal = ["#E9DFC8", "#F2C27A", AMB, RED, INK]
def lvl(c):
    if c == 0: return 0
    return 1 if c <= t1 else 2 if c <= t2 else 3 if c <= t3 else 4
cell, gap = 12, 3
ox, oy = (W - 53 * (cell + gap) + gap) // 2, 196
for wi, w in enumerate(cal["weeks"]):
    for di, d in enumerate(w["contributionDays"]):
        wd = dt.date.fromisoformat(d["date"]).isoweekday() % 7
        o.append(f'<rect class="c" x="{ox+wi*(cell+gap)}" y="{oy+wd*(cell+gap)}" width="{cell}" height="{cell}" rx="2" fill="{pal[lvl(d["contributionCount"])]}" style="animation-delay:{0.5+wi*0.025:.2f}s"><title>{d["date"]}: {d["contributionCount"]}</title></rect>')
o.append('</svg>')
os.makedirs("dist", exist_ok=True)
open("dist/stats.svg", "w").write("\n".join(o))
print(year_total, life, cur, longest, repos, stars)
