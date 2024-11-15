import re
import pandas as pd
from tabulate import tabulate


def parse_report(report):
    routes = []
    pattern = r"(●|○|ƒ)\s+(/\S+)\s+(\d+(?:\.\d+)?)\s+kB\s+(\d+(?:\.\d+)?)\s+kB"

    for line in report.splitlines():
        match = re.search(pattern, line)
        if match:
            route_type, route, size, first_load_js = match.groups()
            routes.append({
                "Route": route,
                "Size (kB)": float(size),
                "First Load JS (kB)": float(first_load_js)
            })

    return pd.DataFrame(routes)


def compare_builds(old_report, new_report):
    old_df = parse_report(old_report).set_index("Route")
    new_df = parse_report(new_report).set_index("Route")

    merged_df = old_df.join(new_df, lsuffix='_old', rsuffix='_new', how="outer").fillna(0)
    merged_df["Size Diff (kB)"] = merged_df["Size (kB)_new"] - merged_df["Size (kB)_old"]
    merged_df["JS Diff (kB)"] = merged_df["First Load JS (kB)_new"] - merged_df["First Load JS (kB)_old"]

    merged_df.reset_index(inplace=True)
    merged_df = merged_df.rename(columns={
        "Size (kB)_old": "Old Size (kB)",
        "Size (kB)_new": "New Size (kB)",
        "First Load JS (kB)_old": "Old JS (kB)",
        "First Load JS (kB)_new": "New JS (kB)"
    })

    # Filter routes with differences
    diff_df = merged_df[(merged_df["Size Diff (kB)"] != 0) | (merged_df["JS Diff (kB)"] != 0)]

    return diff_df


def colorize_diff(df):
    def colorize(value):
        if value > 0:
            return f"\033[91m{value:.2f}\033[0m"  # Red for increases
        elif value < 0:
            return f"\033[92m{value:.2f}\033[0m"  # Green for decreases
        return f"{value:.2f}"  # No change

    df["Size Diff (kB)"] = df["Size Diff (kB)"].apply(colorize)
    df["JS Diff (kB)"] = df["JS Diff (kB)"].apply(colorize)
    return df
# Example usage
old_report = """ 
Route (pages)                                      Size     First Load JS
┌ ● /                                              11.7 kB         381 kB
├   └ css/ef7299afc80df0ed.css                     1.18 kB
├   /_app                                          0 B             224 kB
├ ○ /404                                           2.7 kB          310 kB
├ ● /500                                           2.72 kB         310 kB
├ ● /account                                       7.65 kB         481 kB
├ ● /account/addresses                             4.01 kB         402 kB
├ ● /account/cards                                 7.1 kB          370 kB
├ ● /account/change-password                       3.42 kB         351 kB
├ ● /account/communication                         4.72 kB         389 kB
├ ● /account/corporation-profile                   3.37 kB         352 kB
├ ● /account/create-password                       3.34 kB         351 kB
├ ● /account/family-code                           23 kB           368 kB
├ ƒ /account/orders                                8.35 kB         395 kB
├ ƒ /account/orders/refund/[orderId]               6.38 kB         369 kB
├ ● /account/orders/refund/successful              4.64 kB         349 kB
├ ● /account/profile                               4.26 kB         408 kB
├ ● /account/profile/delete-account                3.55 kB         392 kB
├ ƒ /account/subscription/detail/[id]              4.23 kB         421 kB
├ ƒ /account/subscription/edit/[id]                11.2 kB         468 kB
├ ● /account/subscription/order-immediate-success  4.1 kB          349 kB
├ ƒ /account/subscription/skip/[id]                6.81 kB         358 kB
├ ƒ /api/auth/[...nextauth]                        0 B             224 kB
├ ƒ /api/invoice-request                           0 B             224 kB
├ ƒ /api/private/calculate                         0 B             224 kB
├ ƒ /api/private/getAllOrders                      0 B             224 kB
├ ƒ /api/private/getLastOrder                      0 B             224 kB
├ ƒ /api/private/getUnReviewedProducts             0 B             224 kB
├ ƒ /api/private/uploadFile                        0 B             224 kB
├ ƒ /api/robots                                    0 B             224 kB
├ ● /auth/forgot-password                          4.25 kB         312 kB
├ ƒ /auth/login                                    6.03 kB         447 kB
├ ● /auth/logout                                   500 B           224 kB
├ ● /auth/reset-password                           5.17 kB         313 kB
├ ● /auth/sign-up                                  21 kB           421 kB
├ ● /cart                                          19.7 kB         482 kB
├ ● /charity                                       2.74 kB         352 kB
├ ● /charity/application-final-step                3.51 kB         311 kB
├ ● /charity/application-first-step                2.28 kB         336 kB
├ ● /charity/application-second-step               2.28 kB         336 kB
├ ● /charity/application-summary-step              5.78 kB         343 kB
├ ● /charity/application-third-step/account        535 B           500 kB
├ ● /charity/application-third-step/address        536 B           500 kB
├ ● /charity/application-third-step/subscription   538 B           500 kB
├ ● /checkout                                      1.05 kB         304 kB
├   └ css/7ec58a8ebb2153ac.css                     914 B
├ ● /checkout/address                              9.54 kB         510 kB
├ ● /checkout/payment                              10.9 kB         436 kB
├ ● /checkout/subscriptions                        4.05 kB         388 kB
├ ● /custom-packet                                 6.2 kB          428 kB
├ ● /debug                                         2.45 kB         310 kB
├ ƒ /debug/error-mock                              2.61 kB         310 kB
├ ƒ /debug/info                                    582 B           225 kB
├ ● /donation-culture                              773 B           350 kB
├ ● /know-us/all-materials                         13.3 kB         327 kB
├ ● /know-us/cookies                               7.21 kB         315 kB
├ ● /know-us/faqs                                  3.33 kB         325 kB
├ ƒ /know-us/faqs/[slug]                           1.18 kB         323 kB
├ ● /know-us/how-it-works                          4.45 kB         356 kB
├ ● /know-us/kvkk                                  11.5 kB         319 kB
├ ● /know-us/membership-agreement                  2.23 kB         317 kB
├ ● /know-us/price-policy                          2.32 kB         374 kB
├   └ css/707ba2e7b96b0a82.css                     1.66 kB
├ ● /know-us/privacy                               2.22 kB         317 kB
├ ● /know-us/terms-of-use                          7.96 kB         315 kB
├ ● /know-us/test-results                          4.62 kB         312 kB
├ ● /know-us/why-beije                             1.34 kB         351 kB
├ ƒ /landing/otp/pad                               2.53 kB         423 kB
├ ● /landing/otp/popular                           1.5 kB          407 kB
├ ƒ /landing/subscription/pad                      2.27 kB         416 kB
├ ƒ /landing/subscription/pad2                     9.48 kB         469 kB
├ ƒ /landing/trial-pads                            4.27 kB         461 kB
├ ƒ /landing/trial-tampons                         4.27 kB         461 kB
├ ƒ /packet/[slug]                                 10.5 kB         476 kB
├ ● /packets                                       2.38 kB         410 kB
├ ƒ /packets/[slug]                                1.63 kB         409 kB
├ ● /packets/popular                               1.75 kB         410 kB
├ ƒ /product/[pageIdentifier]                      20.1 kB         485 kB
├   └ css/792033c9858fd269.css                     1.52 kB
├ ƒ /purchase/success/order/[orderId]              5.03 kB         350 kB
├ ƒ /purchase/success/subscription                 4.11 kB         349 kB
├ ● /quiz                                          4.28 kB         312 kB
├ ● /quiz/email-step                               420 B           316 kB
├ ● /quiz/fifth-step-current-products              7.91 kB         315 kB
├ ● /quiz/final-step-product-questions             432 B           316 kB
├ ● /quiz/fourth-step-period-intensity             4.16 kB         318 kB
├ ƒ /quiz/result/[quizId]                          7.45 kB         380 kB
├   └ css/dae683052d9c892f.css                     1.19 kB
├ ● /quiz/second-step-period-duration              4.34 kB         312 kB
├ ● /quiz/sixth-step-daily-product-usage           6.92 kB         319 kB
├ ● /quiz/third-step-period-last                   4.24 kB         312 kB
├ ● /store                                         1.59 kB         357 kB
└ ƒ /store/[typeSlug]/[productSlug]                7.15 kB         378 kB
    └ css/4a0e03c47bffe4df.css                     1.36 kB
+ First Load JS shared by all                      225 kB
  ├ chunks/framework-c865606278fca110.js           45.2 kB
  ├ chunks/main-92d7fb0508add336.js                37.8 kB
  ├ chunks/pages/_app-c47e325eab489e05.js          137 kB
  └ other shared chunks (total)                    4.52 kB

ƒ Middleware                                       42.1 kB
"""
new_report = """  
Route (pages)                                      Size     First Load JS
┌ ● /                                              11.7 kB         381 kB
├   └ css/ef7299afc80df0ed.css                     1.18 kB
├   /_app                                          0 B             224 kB
├ ○ /404                                           2.7 kB          313 kB
├ ● /500                                           2.72 kB         313 kB
├ ● /account                                       7.02 kB         481 kB
├ ● /account/addresses                             4 kB            402 kB
├ ● /account/cards                                 7.09 kB         371 kB
├ ● /account/change-password                       3.42 kB         354 kB
├ ● /account/communication                         4.68 kB         391 kB
├ ● /account/corporation-profile                   3.37 kB         354 kB
├ ● /account/create-password                       3.34 kB         354 kB
├ ● /account/family-code                           23 kB           370 kB
├ ƒ /account/orders                                8.35 kB         395 kB
├ ƒ /account/orders/refund/[orderId]               6.38 kB         372 kB
├ ● /account/orders/refund/successful              4.64 kB         352 kB
├ ● /account/profile                               3.69 kB         410 kB
├ ● /account/profile/delete-account                3.15 kB         394 kB
├ ƒ /account/subscription/detail/[id]              5.44 kB         422 kB
├ ƒ /account/subscription/edit/[id]                10.1 kB         468 kB
├ ● /account/subscription/order-immediate-success  4.1 kB          352 kB
├ ƒ /account/subscription/skip/[id]                6.12 kB         360 kB
├ ƒ /api/auth/[...nextauth]                        0 B             224 kB
├ ƒ /api/invoice-request                           0 B             224 kB
├ ƒ /api/private/calculate                         0 B             224 kB
├ ƒ /api/private/getAllOrders                      0 B             224 kB
├ ƒ /api/private/getLastOrder                      0 B             224 kB
├ ƒ /api/private/getUnReviewedProducts             0 B             224 kB
├ ƒ /api/private/uploadFile                        0 B             224 kB
├ ƒ /api/robots                                    0 B             224 kB
├ ● /auth/forgot-password                          4.25 kB         314 kB
├ ƒ /auth/login                                    6.03 kB         449 kB
├ ● /auth/logout                                   500 B           224 kB
├ ● /auth/reset-password                           5.17 kB         315 kB
├ ● /auth/sign-up                                  21 kB           423 kB
├ ● /cart                                          19.6 kB         483 kB
├ ● /charity                                       2.74 kB         355 kB
├ ● /charity/application-final-step                3.5 kB          314 kB
├ ● /charity/application-first-step                2.28 kB         338 kB
├ ● /charity/application-second-step               2.27 kB         338 kB
├ ● /charity/application-summary-step              5.78 kB         346 kB
├ ● /charity/application-third-step/account        534 B           502 kB
├ ● /charity/application-third-step/address        536 B           502 kB
├ ● /charity/application-third-step/subscription   538 B           502 kB
├ ● /checkout                                      1.05 kB         304 kB
├   └ css/7ec58a8ebb2153ac.css                     914 B
├ ● /checkout/address                              9.54 kB         509 kB
├ ● /checkout/payment                              7.4 kB          436 kB
├ ● /checkout/subscriptions                        4.05 kB         387 kB
├ ● /custom-packet                                 6.2 kB          428 kB
├ ● /debug                                         2.45 kB         313 kB
├ ƒ /debug/error-mock                              2.6 kB          313 kB
├ ƒ /debug/info                                    582 B           225 kB
├ ● /donation-culture                              773 B           353 kB
├ ● /know-us/all-materials                         13.3 kB         329 kB
├ ● /know-us/cookies                               7.2 kB          317 kB
├ ● /know-us/faqs                                  3.33 kB         328 kB
├ ƒ /know-us/faqs/[slug]                           1.18 kB         326 kB
├ ● /know-us/how-it-works                          4.45 kB         359 kB
├ ● /know-us/kvkk                                  11.5 kB         322 kB
├ ● /know-us/membership-agreement                  2.22 kB         320 kB
├ ● /know-us/price-policy                          2.31 kB         374 kB
├   └ css/707ba2e7b96b0a82.css                     1.66 kB
├ ● /know-us/privacy                               2.21 kB         319 kB
├ ● /know-us/terms-of-use                          7.95 kB         318 kB
├ ● /know-us/test-results                          4.62 kB         315 kB
├ ● /know-us/why-beije                             1.34 kB         353 kB
├ ƒ /landing/otp/pad                               2.53 kB         423 kB
├ ● /landing/otp/popular                           1.49 kB         407 kB
├ ƒ /landing/subscription/pad                      2.27 kB         416 kB
├ ƒ /landing/subscription/pad2                     9.47 kB         469 kB
├ ƒ /landing/trial-pads                            4.27 kB         461 kB
├ ƒ /landing/trial-tampons                         4.27 kB         461 kB
├ ƒ /packet/[slug]                                 7.44 kB         476 kB
├ ● /packets                                       2.38 kB         411 kB
├ ƒ /packets/[slug]                                1.63 kB         410 kB
├ ● /packets/popular                               1.75 kB         410 kB
├ ƒ /product/[pageIdentifier]                      17.2 kB         486 kB
├   └ css/792033c9858fd269.css                     1.52 kB
├ ƒ /purchase/success/order/[orderId]              5.02 kB         350 kB
├ ƒ /purchase/success/subscription                 4.1 kB          350 kB
├ ● /quiz                                          4.27 kB         314 kB
├ ● /quiz/email-step                               420 B           318 kB
├ ● /quiz/fifth-step-current-products              7.91 kB         318 kB
├ ● /quiz/final-step-product-questions             432 B           318 kB
├ ● /quiz/fourth-step-period-intensity             4.16 kB         321 kB
├ ƒ /quiz/result/[quizId]                          7.44 kB         380 kB
├   └ css/dae683052d9c892f.css                     1.19 kB
├ ● /quiz/second-step-period-duration              4.33 kB         314 kB
├ ● /quiz/sixth-step-daily-product-usage           6.92 kB         321 kB
├ ● /quiz/third-step-period-last                   4.24 kB         314 kB
├ ● /store                                         1.58 kB         358 kB
└ ƒ /store/[typeSlug]/[productSlug]                7.15 kB         378 kB
    └ css/4a0e03c47bffe4df.css                     1.36 kB
+ First Load JS shared by all                      225 kB
  ├ chunks/framework-c865606278fca110.js           45.2 kB
  ├ chunks/main-92d7fb0508add336.js                37.8 kB
  ├ chunks/pages/_app-fa13e7e33abc526f.js          137 kB
  └ other shared chunks (total)                    4.51 kB

ƒ Middleware                                       42.1 kB
"""



df = compare_builds(old_report, new_report)
colored_df = colorize_diff(df)
print(tabulate(colored_df, headers="keys", tablefmt="grid", showindex=False))

