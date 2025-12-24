Request URL
http://localhost:8000/api/v1/research
Request Method
POST
Status Code
200 OK

{entity_name: "Tesla", entity_type: "company",…}
entity_name
: 
"Tesla"
entity_type
: 
"company"
research_types
: 
["financial", "sentiment", "news", "personality", "market_analysis", "social_media", "career",…]
selected_providers
: 
["google_news", "linkedin", "wikipedia", "duckduckgo", "reddit", "github", "instagram", "youtube",…]


{
    "entity_name": "Tesla",
    "entity_type": "company",
    "results": [
        {
            "research_type": "financial",
            "title": "Financial Analysis",
            "data": {
                "_raw_search_results": [
                    {
                        "title": "Earnings live: S&P 500 on track for highest revenue growth in 3 years, with reports from Deere, Zoom ahead - Yahoo Finance",
                        "link": "https://news.google.com/rss/articles/CBMi4AFBVV95cUxOZVU5QW44TElTSHEyRFlCZVpwY1hZYmZKZFI3dmtpcEd1b2JHWC1Tckh3dmM1encyT0M2QzZibnBvSzh1OHZjaVhPUVY4MmNLdV9uQUdndmJUMlRSQU5DVjNMMGE5TEhSX2hlZVd3d0lHa3BVMldUaVJEWUZBZnExVnFGc3NoRW5QOExQc2JYdnRJV3d6S0t0dzdpX0kzYUtELVQzNEZ6bXlldjJiNUQzMUQzMUxzZ0dzZTNSSWhPZ3dVbXdIZzBjYkt5cG12cEdDTXVYN3pFV1JEMk1YTEx1Qg?oc=5",
                        "published_date": "Fri, 21 Nov 2025 21:23:39 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Tesla Rides High Before Q3 Earnings With (TSLA) Stock Rising, Record Deliveries, Gigafactory Growth, and Green Goals - CarbonCredits.com",
                        "link": "https://news.google.com/rss/articles/CBMi1AFBVV95cUxOZm5PM0FpV0RPRjgxZ2ZmSlRrcnNEeUFfb1J4bzlrY2pUemMzbWNqWVBqNjA5cWkxUlZmQWUyd1VmODZUeVZvSkR4cWtKOE52aW10Y0xYVEtoZTJPOExzMGpFVXAxWmpDZUxFcnJQSW81amFhVnJwek0tcmREZDl3d2xOc3RTc2hWRzFvejNibHJwRklQTWV2OTNFNm9vT3ZNeEo0amlzd21TUWQ0dXZPZWJ3YXhwb0QtSm82VEVRSjNsX3dqekhlSnpKdjYwM01DY09Jbw?oc=5",
                        "published_date": "Mon, 20 Oct 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Tesla Earnings Miss, Elon Musk Sees Unsupervised Robotaxis By Year-End, But TSLA Slides - Investor's Business Daily",
                        "link": "https://news.google.com/rss/articles/CBMijAFBVV95cUxOa3FXMmdwaDB6cllraFJ1WXR3R3JmNGxxaDUyU1hMRk5aY1dFNWk2bEpQUVYtdDhxOW5uZ1dwSzJBMWNJaXRHUUdldjFWQ3NVRmFURVRIbG1HT213LTlqNEVJaG5fUlZNcmxqbHZEZnQ2OThWRkNvTXc2NjNIOXNkRnM2VGQzUlUtOFplOQ?oc=5",
                        "published_date": "Thu, 23 Oct 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Wikipedia: List of public corporations by market capitalization",
                        "link": "https://en.wikipedia.org/wiki/List_of_public_corporations_by_market_capitalization",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "The following is a list of publicly traded companies, that have the largest market capitalization or sometimes described as their \"market value\".\nMarket capitalization is calculated by multiplying the share price on a selected day and the number of outstanding shares on that day."
                    },
                    {
                        "title": "Wikipedia: History of Tesla, Inc.",
                        "link": "https://en.wikipedia.org/wiki/History_of_Tesla,_Inc.",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Tesla, Inc. is an electric vehicle manufacturer and clean energy company founded in San Carlos, California in 2003 by American entrepreneurs Martin Eberhard and Marc Tarpenning."
                    },
                    {
                        "title": "Wikipedia: Meta Platforms",
                        "link": "https://en.wikipedia.org/wiki/Meta_Platforms",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Meta Platforms, Inc. (DBA Meta) is an American multinational technology company headquartered in Menlo Park, California."
                    }
                ]
            },
            "summary": "Analysis completed for Tesla",
            "confidence": 1.0,
            "timestamp": "2025-12-24T16:34:26.053783"
        },
        {
            "research_type": "sentiment",
            "title": "Sentiment Analysis",
            "data": {
                "_raw_search_results": [
                    {
                        "title": "Thanks, Elon—It Sure Is Weird Being a Tesla Owner Right Now - MotorTrend",
                        "link": "https://news.google.com/rss/articles/CBMixAFBVV95cUxNWENKdjFYSHpQWDd6YTBsbmJST1RFMmtrRXJ6SUswZ05oSEpoUVZaUkFpcXBNU3JES0l1NVhscThQMHZTRUlETGI4cTR5VGd1Z0d5ZzBJWWtHVVdhTXA2R012bzFCUWZTNXpZSXhYOFI4UHJUekh0VGxTR3NuTE5hMnFOdVZydjg5MmJKZ0xSMG9aQWNiYjZIMHE5dGV4ZFR6dUpUUTVnMmhZQUVtUFpNX2h6ZDA2aTBxNEJjaVN5Q29tWTlI?oc=5",
                        "published_date": "Thu, 03 Apr 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Tesla faces growing negative perception, latest survey shows - ArenaEV - ArenaEV",
                        "link": "https://news.google.com/rss/articles/CBMigwFBVV95cUxOQ3J0MUJ5ZFV1T2JUY2RwTjVEUVZWc01UWmNYN21MUGYwckFlVXk0amU1b3E3Mm0tWm52bENPU21JTFA3MjFfQlZfZXQ4N1Ytc0Z4QlhRYWM3WklLazM4dEtHbW5qTzNwZW9sM2xtLWhxbW5EeGFaOWJrNndrVGVwWkNpSdIBf0FVX3lxTE05VXhNUUdCeHRMZmE4WVEwVk5pVDdNbnZuQmJmVkVXdHRUX3dnbW5yRmg5dDVxdFhxN0NYRXkxMHJtSHVqMzFEb0tNUmJrejVNOXdhUi1wSVpVTkNvd2UxenZCLU9jTkMySlg4RF94enljeHI4XzloeEk1bmw0VjA?oc=5",
                        "published_date": "Fri, 02 May 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Tesla registrations — and public opinion — are in a free fall - The Verge",
                        "link": "https://news.google.com/rss/articles/CBMiiwFBVV95cUxQZkVjUlFtUTYxaHVuaG04eTNCWE5tbWdqbU10Z2RUZ01KUENSbkpyOVRKVFplM3V2RGhfRjVFdHVKY2ZrMS1LWHRyS3paNGQ4b3dvZ29rM0pRZXI5NlF2bWozRzZfbWY1OEdqdV9RTUEySjRKSHd4RHhJcmdBWVhyeFl2dlpLYTV6X1Jr?oc=5",
                        "published_date": "Fri, 14 Mar 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Wikipedia: Second presidency of Donald Trump",
                        "link": "https://en.wikipedia.org/wiki/Second_presidency_of_Donald_Trump",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Donald Trump's second and current tenure as the president of the United States began upon his inauguration as the 47th president on January 20, 2025. Trump, a member of the Republican Party, had previously served as the 45th president from 2017 to 2021 and lost re-election to the Democratic nominee Joe Biden in the 2020 presidential election, took office after defeating the Democratic incumbent vice president Kamala Harris in the 2024 presidential election."
                    },
                    {
                        "title": "Wikipedia: Chinese Exclusion Act",
                        "link": "https://en.wikipedia.org/wiki/Chinese_Exclusion_Act",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "The Chinese Exclusion Act of 1882 was a United States federal law signed by President Chester A. Arthur on May 6, 1882, prohibiting all immigration of Chinese laborers for 10 years. The law made exceptions for travelers and diplomats."
                    },
                    {
                        "title": "Wikipedia: List of topics characterized as pseudoscience",
                        "link": "https://en.wikipedia.org/wiki/List_of_topics_characterized_as_pseudoscience",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "This is a list of topics that have been characterized as pseudoscience by academics or researchers. Detailed discussion of these topics may be found on their main pages."
                    }
                ]
            },
            "summary": "Analysis completed for Tesla",
            "confidence": 1.0,
            "timestamp": "2025-12-24T16:34:32.493391"
        },
        {
            "research_type": "news",
            "title": "News Analysis",
            "data": {
                "recent_news": [
                    {
                        "headline": "Report Focuses on Deaths Due to Tesla Doors That Couldn't Be Opened Following a Crash - Car and Driver",
                        "date": "Mon, 22 Dec 2025 21:28:40 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMiiwFBVV95cUxNRTluRGxYQWkzSWU0aTRpdW1vVk1OYi1hN0NWQzBMSjJRa0ZpaWpSR2R6SUdiNTNUVGU1THNlM19nQktjRHQ5LWEyNl9oRUFMZHo3ZGdyX1NLazlyMUtkdlNkLUhhaURVV1FBSFphbFRESF9qakVxVmtvYzdfZU1RajBKeGV5dEZKT0ln?oc=5"
                    },
                    {
                        "headline": "Elon Musk Demanded Tesla’s Electric Doors Despite Safety Worries - Bloomberg.com",
                        "date": "Mon, 22 Dec 2025 22:00:08 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMirgFBVV95cUxQQi1PLUlLUlAtazgxenprcFF0Um9FZ2lGbkJvblRwQ2ZpY000VnJMeUp6eDZ6MXpCbzl2bFFYeEFMOU1GTFNQVXA0TDVLckdtVlU4WEUtbWh6MGxzUjdlemRBYzhXUzNQV1JRRkZkdS1nblBYT3BlbjVLYndMalZVWGl6alZNYUVtUGRiS1g0dkF6dTB1X2lTQXAzcU9vdk04cFJBeTVUcDNpZTJIZ1E?oc=5"
                    },
                    {
                        "headline": "The Dark Side Of Tesla's Sleek Door Handle Tech - InsideEVs",
                        "date": "Wed, 24 Dec 2025 03:04:27 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMie0FVX3lxTE45Tk1YeGJUSUlQYmcyTF96MW50dVNDcmdrT1YwYTVmUmh3eDZDaC1CWG1QT25xaHlJX2c1MlkxZWJMT2FrbHpsZ0NpNEp2enRZX1FlSktLa19xNE5wUEhXUHM1RWQ5N2YwdVN5RkFpc3JhZkpqVTZRMmFYWQ?oc=5"
                    },
                    {
                        "headline": "Tesla’s EU sales slump continues as Chinese rivals thrive - The Guardian",
                        "date": "Tue, 23 Dec 2025 20:02:00 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMiqgFBVV95cUxQRG9NejlqeThOc2R6UDFCMTdoV0tOZmk0Mmh4TGhKR0VGOHpzeFVoYU9oczBlZ1lFM2ZfTVprdm13OUhBdGlWaVRMYlZxTmVaTkdSd1RmZEI2M2JWS1lDZlJnZVEybTUycDBITDJSZHptcGhuZHhsd01zMlBWc1hRMENkNlpSTTlkVGtZZU81enJtNVJBR2wwSGlBSGRUQWZYQUgwS09MWGFHUQ?oc=5"
                    },
                    {
                        "headline": "Tesla’s EV sales keep falling, but Wall Street stays focused on robotaxis - MarketWatch",
                        "date": "Tue, 23 Dec 2025 16:26:00 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMiugNBVV95cUxPejcydlV0emRRT09GYWNYNTFqeGtsNHl4eFk3TjRNUUdFaHNGMUlVYVJoQXRPVzhFaXF5Q3h4WDQ0d3pJcFhQRlUzMmxleU1iWkhNUEx0cmFsOG5lSUtDanR3b1JlTWRJWm01cVUzVkhGQXRsMkxpbkU5cHFFY3k0Wk8zTXRCNVJ6WVdBYl9VYTZibk4wYXdUQ3AzUXd0TVQtSnB6WGUydEptZnJ1aUV3LTJvOUhMUERUVnNzczNMRTR2TE5xOGtGeUV1ZGU3T2tZUXZrMm45RHlzX2poMmFMOHVyQmtMQjlOUld6eFlld2I1dXpKNmN2d0hMeWxGMjc2N2t1WDNMcmxHM0xjQ3JWMkgzX3lkWF9QQjlSMms4MWp2akNULUVSQ0hZSzdBcmt3Mkh6U3cwUU9Qck5BZEJqS1Y0VEc1aHJvclVIYkxPaFAzS3lRWGQ4Q204Zk1LY3hZeVF5M2NZWUJfNmxERVZncUVEWExVd0RLRU1fWEhyR0pJVzdWMW53WDdxSkdiYzc0bjBlTTBfdS1nLXM3b0FNN1lYQ1lQTGJfa3ZxME9FY19rRmN2ZWd4cnhn?oc=5"
                    },
                    {
                        "headline": "Tesla Loses Ground in Europe as BYD Sales Surge 222% - Yahoo Finance",
                        "date": "Tue, 23 Dec 2025 15:45:23 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMigAFBVV95cUxNY1Q0WG00ZXlQOXNGdUdQeTVPVDBJZ3JiMUp1OVYxWDdsVmM4Vmc5NzFnNHNNRjM4OE1NU0gyS0gxTVo3Zk1HVXg2Yy1QZC1lVThrSm5nbm1tNGlYYnpGdmhzbUxIZnFiMTJiZV9wMTBLd1c0ZWlEWXd6cnFQMVdWcQ?oc=5"
                    },
                    {
                        "headline": "Ford, Hyundai and yes, Tesla make the list for best-selling SUVs of 2025. See the list - USA Today",
                        "date": "Wed, 24 Dec 2025 10:06:00 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMiugFBVV95cUxORVVRcDdmc1RBM3EzQ0lkZjFKRnpRY1FFTDdES1FybUhhSnRvdjBxWUtpODV4YTRhQTNaMnkzYURfNl9LU3VOUW5WYXZlTTE0cXp2NlZDS3hFTkFpR0pURWlzZ0g1SlRKT05rXy05czMwVFljWlN3eG1wakZDcThzbDc4bzl3UExudGdVNk9UaTE2NGcyd19pSUVMdFV4V2dubTgxYWdWZkJid0dlWkZCelEtRFg0aXM0VkE?oc=5"
                    },
                    {
                        "headline": "Tesla Comes One Step Closer to Self-Driving With a New Camera Patent - Autoblog",
                        "date": "Tue, 23 Dec 2025 19:30:00 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMigAFBVV95cUxQcVNIbVEyYXhueEZkNnFfT2t5YVJiQkJack1KOUNrWHNNWkQteUI2RnVVWEhHZEdza05FQS1FeHk5WG1TTFViTHVLVmJGMWhlcXZKbm14eG5hVXdmUXJESHRTVWdyeG9ycnBLVFdWcGV6ZURHZWZtRDYzbEFjZXBzOQ?oc=5"
                    },
                    {
                        "headline": "Tesla driver crashes during livestream desmonstrating ‘Full Self-Driving’ features - Electrek",
                        "date": "Tue, 23 Dec 2025 19:43:00 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMiqAFBVV95cUxNMmhwdkZ1RUV1bUtBVVRKNnM4R2UycTlsSlE0RDdxbTRwUlJ6bEF4M0Z6VWFBN2w4OUxmTWhiMVBWendaR25XdWJBcFFBTFdUX1FyNUdjSzhYVmoyQjV4ejNDaFVYbWVRSV9XRF9jUDJfWHFOSjlLTHB0a2xXSE5uRThIMlJOMV9udzM5UVRUNnhjTkR6WWgzdWpWODZxT1djdmJVUVZ2U0c?oc=5"
                    },
                    {
                        "headline": "Opinion: I tried Tesla Autopilot on home turf, and it behaved way better than in Britain - Top Gear",
                        "date": "Tue, 23 Dec 2025 05:05:22 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMitwFBVV95cUxQLWlhOUNnUGNHanVlYmVHaDE1ellyaTN0RWUtb1dZYlNOZkFCZU9nOExZQnE4bUJZNElNblp2UjJIV04tNXowNjJKWWoxLTJURlRYSUhVZi1BLXduSjd4OTdSQzFxU0JXOWpFOFROclBiOEJfalNjSXZOajhkX3Y1Q1MxQnlFRGx3Znd3NFRETm9qWTBmcHB6c3h1ejQ3Rmc1el9LZGUwLUNKSXQzeUNUVXdBS1dVdWM?oc=5"
                    }
                ],
                "total_articles": 10,
                "press_releases": 0,
                "media_mentions": 0,
                "trending_topics": [],
                "sentiment_breakdown": {
                    "positive": "0%",
                    "neutral": "0%",
                    "negative": "0%"
                }
            },
            "summary": "Tesla has 10 recent articles analyzed.",
            "confidence": 0.5,
            "timestamp": "2025-12-24T16:34:33.754407"
        },
        {
            "research_type": "personality",
            "title": "Personality Analysis",
            "data": {
                "_raw_search_results": [
                    {
                        "title": "From Jeff Bezos to Elon Musk: Zodiac signs of richest billionaires in the world unveiled - Times of India",
                        "link": "https://news.google.com/rss/articles/CBMiiAJBVV95cUxPQ0w2bHBOUFpNQUJubnFXdTFNcGFreC1pXzJzT1NKQnB5SVpjdHBvUno0RDc3RUpBZHZSeTlyWUFDRnl5WTNpS2lqV1BhbS1SVEI1UFdwSXpLYnQ3ZlhTN3g2SWpucnJTTzRlVnZvWW5mcjQ5V3haT2swRUxRZ1JGMWQ5Rzl0cS0tdjVfeTdOV3NKelQtd2ljcGc3eHhZQ3hfeWpQMEtOTmxQN0d1dXZxN0JjYjE0OG5FMk16aXdUTmJ3Ti1CTzRVWW1CcGhIUzA0bHMwWkdTb1hOQWhJWmp2MWNPN0dKeU1QTmVRVTJpSHJfYWNPTjVlMnRsa09HMWtHc1o5SUFmY2vSAY4CQVVfeXFMTlE2Ym51QVkyRzNPNExidTQtUmxha3VnU2M5eXhncWRkMnNmRWd3YUNMTW1UYk9VWE5uR2FyeUhUczQ4akR1N1pXRkJtLVBKTDBUMnZnam54VldCM3RQSFV5WXVjRW5xZXAxVFo3ekpfeEw3RlZBU1JfZ2dsWDFjUklPdVhwMjlGcC1BeU11ZjROT1BQcFZCejUxMjhnS1FidGJsVjZSUmhmRzNvaVlkakplUDB1Q0VkdzlLSWxweUN6S2ItVUxNV1UtTVhoSk9iRE0tRzRyM29pZUFKd1ZKdktvUHM4Wk9SM2JLUGxVdmduc3MxVTVOVE1LYUNGMld2dzhZam1wel9hZUtGVUpR?oc=5",
                        "published_date": "Thu, 05 Jun 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Elon Musk’s Leadership Style Bad For Business And Mental Health, Experts Warn - Forbes",
                        "link": "https://news.google.com/rss/articles/CBMiygFBVV95cUxPOTlCQ0xyd2lYdVprTG1LRDBXRGNtbk9TWl8xS1J6Q1M5NFF3YnY5dzFrUXE2NUozbzVjaWVBWGJGQTFDWV8ySFFhdVJUNE5Sb1VjYl9veDJkTzc3Rlo0cE5MdVRtTkx0Y2NtNDFtRzVwVHQzakw1R0lHbGE3a250NFRDWllibkZaTldNYjhGSWcyQnVUSEJJX3dSb2lxMERpNnZfb1hUS25hRk93WDdqVEJ1eDNscWk1bHNvQWJNZGY1bTVacFlyWUln?oc=5",
                        "published_date": "Mon, 21 Nov 2022 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Elon Musk’s Leadership Gaps At Tesla Come To A Head - CleanTechnica",
                        "link": "https://news.google.com/rss/articles/CBMikgFBVV95cUxNZnBlMzlYYWtYdXNXSU12QkNNRDlNcTM5akRRRTBjVzV0NFViQkU2b3ZhNDhTY3NDM2s0dHBJYnFSLXAwQWlVcGd5WWdfaTQwaTk3cURBenc2dG5leC01b0lyNm1XU3pvbEJNSHZ0UEE3TGdZdFBTR0Q0cnR5TkxGV0tkdDd0ck81UkJzRG9KdXJ6d9IBlwFBVV95cUxONzFXd1M2N0RvMk8tZEk3NTJjVS1Uc2FseldyTzVFRzVhTS1vZ3VyYTZRR0FVTlRhVnJzY0N0d015OUNzLXVqbkZyLTVFT1dveFhWbVRIZlRKX2U1aTJtYXNtc2kycW5hRHVwMmdic002UHFfcXZEZ20zN3lsNlNuOER3SGNlbnE4SVdxaHJIejZfUUN4LU5r?oc=5",
                        "published_date": "Wed, 24 Apr 2024 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Wikipedia: Raymond Cattell",
                        "link": "https://en.wikipedia.org/wiki/Raymond_Cattell",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Raymond Bernard Cattell (20 March 1905 – 2 February 1998) was a British-American psychologist, known for his psychometric research into intrapersonal psychological structure. His work also explored the basic dimensions of personality and temperament, the range of cognitive abilities, the dynamic dimensions of motivation and emotion, the clinical dimensions of abnormal personality, patterns of group syntality and social behavior, applications of personality research to psychotherapy and learning theory, predictors of creativity and achievement, and many multivariate research methods including the refinement of factor analytic methods for exploring and measuring these domains."
                    },
                    {
                        "title": "Wikipedia: Cult of personality",
                        "link": "https://en.wikipedia.org/wiki/Cult_of_personality",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "A cult of personality, or a cult of the leader, is the result of an effort to create an idealized and heroic image of an admirable leader, often through unquestioning flattery and praise.\nHistorically, it has been developed through techniques such as the manipulation of the mass media, the dissemination of propaganda, the staging of spectacles, the manipulation of the arts, the instilling of patriotism, and government-organized demonstrations and rallies."
                    }
                ]
            },
            "summary": "Tesla exhibits N/A characteristics with a N/A leadership approach.",
            "confidence": 1.0,
            "timestamp": "2025-12-24T16:34:40.606797"
        },
        {
            "research_type": "market_analysis",
            "title": "Market Analysis",
            "data": {
                "_raw_search_results": [
                    {
                        "title": "Competitor Analysis: Evaluating Tesla And Competitors In Automobiles Industry - Benzinga",
                        "link": "https://news.google.com/rss/articles/CBMiygFBVV95cUxQeTBDVHYwMlVRRVNrZVdqTjQ0MlNOS0NvVEMwUlFRdjlDeFZ4UFBmR0I1Njl5M1pEQlJFNFNXWG9KZ0xfeVZELS1kR3JvY0xpT2JGSEpweFh3YkxqVVhHTHQ3UXB0TzQyLUhEN0RwejR1VE5DbEFZa1NVSmYxbG9iR3FCdVp5R2ItbGZmSHVlZDFRWGs1Y29aWGxZNVRqMlI0eHlnaEY1N3VlNkJzTjdFUEtkWUNpc3JoMHhndGJoSTYxNU1NT2NEMWl3?oc=5",
                        "published_date": "Fri, 19 Dec 2025 15:00:25 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Exclusive: Tesla market share in US drops to lowest since 2017 as competition heats up - Reuters",
                        "link": "https://news.google.com/rss/articles/CBMizAFBVV95cUxQbGQ2cnFabmkwd0hNczBsU1JQeWxzcUZfYk9kMWI2TWI5dWZ2ejExX2RFTnQ0blljczMwTEEwSmNVZFZ2dDN2dUxzRS0xM3Azd2hiZ0pvamJzdHhUN0VqbGpneXB6cWVuV2dfNTNJWTUtbGM1Q0x1OEc2Y0s3blpITHhJXzFWRXRBeF9UQTlXTF93ZnVyNjhoQmxIUHFoanJKZ2cweW5mWWlMQzhUMUVzRmVkNjk1T3pwNmtPZ1hFNlZJR250RkM2RGRuVVY?oc=5",
                        "published_date": "Mon, 08 Sep 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Magnificent 7 Stocks: What You Need To Know - Investopedia",
                        "link": "https://news.google.com/rss/articles/CBMibkFVX3lxTFB0SzlzdjZLSVdWbTBqRW9QUTNrRll0YldiOEh5M3J1N2JiUU1BTWZFcFVrc2g4M0NBVXN2MjB5b3gyWm5GSy1zSWpPM2hPTGsxUl9nR0N0OTJuT2hON2ZaTks4cHRnNS0zeldadkVB?oc=5",
                        "published_date": "Fri, 12 Dec 2025 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Wikipedia: History of Tesla, Inc.",
                        "link": "https://en.wikipedia.org/wiki/History_of_Tesla,_Inc.",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Tesla, Inc. is an electric vehicle manufacturer and clean energy company founded in San Carlos, California in 2003 by American entrepreneurs Martin Eberhard and Marc Tarpenning."
                    },
                    {
                        "title": "Wikipedia: Automotive industry in China",
                        "link": "https://en.wikipedia.org/wiki/Automotive_industry_in_China",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "The automotive industry in mainland China has been the largest in the world measured by automobile unit production since 2008. As of 2024, mainland China is also the world's largest automobile market both in terms of sales and ownership."
                    },
                    {
                        "title": "Wikipedia: Criticism of Tesla, Inc.",
                        "link": "https://en.wikipedia.org/wiki/Criticism_of_Tesla,_Inc.",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Tesla, Inc. has been criticized for its cars, workplace culture, business practices, and occupational safety."
                    }
                ]
            },
            "summary": "Tesla holds N/A market share with N/A growth rate.",
            "confidence": 1.0,
            "timestamp": "2025-12-24T16:34:47.115103"
        },
        {
            "research_type": "social_media",
            "title": "Social Media Presence",
            "data": {
                "_raw_search_results": [
                    {
                        "title": "Twitter Users Statistics 2025: Monthly Active Users, Regional Data & More - SQ Magazine",
                        "link": "https://news.google.com/rss/articles/CBMiX0FVX3lxTFAwNi01cEU0M3hpUEFXc2ItSUNJcTdnUkRqU0hKZmNZeFUtc3VWODMydEs3eW9sMXNyTzIySnVLS0R4T3RnTXI2VXJPZ090Yzd3cDZ0U1dWZWVDRHU4cDFz?oc=5",
                        "published_date": "Sun, 21 Dec 2025 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Instagram - statistics & facts - Statista",
                        "link": "https://news.google.com/rss/articles/CBMiW0FVX3lxTE5PUmsyOV8weWJqRVQ5cDRuMWNqYWFvbnVUWFVkU1lnc0pQVjZzVmI1VzVfU2xJSTFMa2ZxRE1kb2tSeG4zTU8xcnM3Z2p1MXBVVXVBZmxlLUJfOG8?oc=5",
                        "published_date": "Wed, 17 Dec 2025 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Topic: Social media usage in the United States - Statista",
                        "link": "https://news.google.com/rss/articles/CBMigwFBVV95cUxNN2t5bTBJTW1HUEpIdVdYVDdrY3NacUplTmYxUXVIeE5wYXRsUVgweHY5OVkzendpWFRCYy1ocE04bzdXeDNtVmdkSzUtR2NjUVg0eFM2SUpLdV9HemZfMlZDWUdHcVpVaUhUQWlfcTNWWm9FN2JCaWNmRFdoMWhneVpQbw?oc=5",
                        "published_date": "Wed, 17 Dec 2025 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Wikipedia: Big Tech",
                        "link": "https://en.wikipedia.org/wiki/Big_Tech",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Big Tech, also referred to as the tech giants or tech titans, is a collective term for the largest and most influential technology companies in the world. It commonly denotes the five dominant firms in the U.S. technology industry—Microsoft, Apple, Alphabet (Google), Amazon, and Meta (Facebook)—which are also the largest companies in the world by market capitalization."
                    },
                    {
                        "title": "Wikipedia: Founders Fund",
                        "link": "https://en.wikipedia.org/wiki/Founders_Fund",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Founders Fund is an American venture capital fund formed in 2005 and based in San Francisco. The fund has roughly $17 billion in total assets under management as of 2025."
                    }
                ]
            },
            "summary": "Tesla has N/A total followers across platforms with an influence score of N/A/10.",
            "confidence": 1.0,
            "timestamp": "2025-12-24T16:34:55.892465"
        },
        {
            "research_type": "career",
            "title": "Career Analysis",
            "data": {
                "_raw_search_results": [
                    {
                        "title": "History of Tesla & its stock: Timeline, facts & milestones - thestreet.com",
                        "link": "https://news.google.com/rss/articles/CBMib0FVX3lxTE1keGZIT0xjZ2lrOWJjRFRNQ2pITW9STWM1OURTZlQzb1RjSTgtSnJ2VjVidFViNkMzXzRkYnpmM05ObGY0ckRMOFY5Tk53Z2RULVV0bFp3Y1dSSUJ1TE1BYjV6RFdkWWppb2h0V3VDQQ?oc=5",
                        "published_date": "Wed, 12 Nov 2025 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "How Tesla can make Elon Musk the world’s first trillionaire - The Week",
                        "link": "https://news.google.com/rss/articles/CBMikAFBVV95cUxNYlp1N3VoVmotamxHWlI2Y2JXaUdKVktoZDAtYzFoNGpudWZ2S3E1Q3BqbGxmTFVPUW83ZDlNUzdsaXNFUEh0MnVXTHpsUmh2dGRUTFhxS1dNSWdwY2ZNbnNlUE40bkNqeHZfRFJKQmtqTTF0NjhOVEh6aHBDdy1tZ2JRRzF3UERZaGxNT2d2cUw?oc=5",
                        "published_date": "Fri, 07 Nov 2025 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Tesla shareholders approve $1 trillion pay package for Elon Musk - NBC News",
                        "link": "https://news.google.com/rss/articles/CBMitgFBVV95cUxPV1F4VFBFNEhJVHN3cnVLXzNXWFNTaDJNRnFIX1RTMzF2M0dRWnd6OFZSYnNjZ0ZiZW5wOElCM2tkcmRITl9RU2FFLXA5aVl0Uk9oOUlEbDgyeUFmcW8zSlpuYy1oUGlscmgyTmh3S3NlR08yc244S2RxRzlRMzlDSU02aEdIMnZ1R3ZKV0RtbU5oVUVXczh2UUJWVzNyaDd3TVotdWFiUjRiZUExTHRwTWtCR1NGUdIBVkFVX3lxTE1tdzh2Z1ozT2ZKckh2OGtrYm1xOUprV0pnNXhpNHFRVHFMandqQ3FsWHdDQWtpRW1Ic1BUSWU0N2J2Z3FkemNEc2gzOVYzY2o3YlhiYzdB?oc=5",
                        "published_date": "Thu, 06 Nov 2025 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Wikipedia: History of Tesla, Inc.",
                        "link": "https://en.wikipedia.org/wiki/History_of_Tesla,_Inc.",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Tesla, Inc. is an electric vehicle manufacturer and clean energy company founded in San Carlos, California in 2003 by American entrepreneurs Martin Eberhard and Marc Tarpenning."
                    },
                    {
                        "title": "Wikipedia: History of the electric vehicle",
                        "link": "https://en.wikipedia.org/wiki/History_of_the_electric_vehicle",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Crude electric carriages were invented in the late 1820s and 1830s. Practical, commercially available electric vehicles appeared during the 1890s."
                    },
                    {
                        "title": "Wikipedia: Tesla, Inc.",
                        "link": "https://en.wikipedia.org/wiki/Tesla,_Inc.",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Tesla, Inc. ( TEZ-lə or   TESS-lə) is an American multinational automotive and clean energy company."
                    }
                ]
            },
            "summary": "Tesla has been operating for N/A with N/A employees.",
            "confidence": 1.0,
            "timestamp": "2025-12-24T16:35:06.324952"
        },
        {
            "research_type": "hobbies",
            "title": "Hobbies & Interests",
            "data": {
                "_raw_search_results": [
                    {
                        "title": "Elon Musk Criticized President Trump’s Spending Bill. Now, He’s Leaving the Administration - Biography",
                        "link": "https://news.google.com/rss/articles/CBMiYkFVX3lxTE83UDVIVndxRW1LaXBJaktxTnlkUWJBT0U3RTdKRHFlTHFjVlFaenQ3SFNJdTkyREFBazBKZmd0MHJzX3VMSGZRUnU5ZjY3d1NSbGgtNWI5cVB2V1NraFdod1VB?oc=5",
                        "published_date": "Thu, 29 May 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Most popular hobbies & activities in the U.S. 2025 - Statista",
                        "link": "https://news.google.com/rss/articles/CBMikgFBVV95cUxNWW1kYS1wbkZLY290WkNxUEZrVnNjaU54NzhrMHV4N3p1MWZtdEFZY1lRcFk5cjBBQ3FXLU1qSE9ZNEFqQUFXN3NmVUEzM0JRczgxb2s0WDNUYTBNUVZEVmNraTV1MHF5em9uM0VaeDdzTS1QQVZ6WlhBZDNiYzJveG9fUVdKdVhEUXN3XzlDRmJlQQ?oc=5",
                        "published_date": "Tue, 25 Nov 2025 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "5 reasons why you should revisit your childhood hobby as an adult - Yahoo Finance",
                        "link": "https://news.google.com/rss/articles/CBMigwFBVV95cUxPWkFfQlBWb0YtY09va29uRExiSXJjc3BwODdlNTdwZzVBZE8tbmV0SW9ZNzZpYXNLR2J1bHJaWUJaYjJadENFc2F0RDhmMGRfTEVDdVQyNjJmNVhydDE1aVBjWHBVVkdES2JnWTNtV0lTSkNOb3czNmlCY0xmU0lnWVZjMA?oc=5",
                        "published_date": "Sat, 25 Feb 2023 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Wikipedia: Influencer",
                        "link": "https://en.wikipedia.org/wiki/Influencer",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "A social media influencer, also known as an online influencer, or simply influencer, is a person who builds a grassroots online presence through engaging content such as photos, videos, and updates. This is done by using direct audience interaction to establish authenticity, expertise, and appeal, and by standing apart from traditional celebrities by growing that person's platform through social media rather than pre-existing fame."
                    },
                    {
                        "title": "Wikipedia: Jef Raskin",
                        "link": "https://en.wikipedia.org/wiki/Jef_Raskin",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Jef Raskin (born Jeff Raskin; March 9, 1943 – February 26, 2005) was an American human–computer interface expert who conceived and began leading the Macintosh project at Apple in the late 1970s.\n\n\n== Early life and education ==\nJef Raskin was born in New York City to a secular Jewish family, whose surname is a matronymic from \"Raske\", Yiddish nickname for Rachel."
                    },
                    {
                        "title": "Wikipedia: Jack London",
                        "link": "https://en.wikipedia.org/wiki/Jack_London",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "John Griffith London (né Chaney; January 12, 1876 – November 22, 1916), better known as Jack London, was an American novelist, journalist and activist. A pioneer of commercial fiction and American magazines, he was one of the first American authors to become an international celebrity and earn a large fortune from writing."
                    }
                ]
            },
            "summary": "Tesla enjoys N/A and is passionate about N/A.",
            "confidence": 1.0,
            "timestamp": "2025-12-24T16:35:19.418443"
        },
        {
            "research_type": "competitor",
            "title": "Competitor Analysis",
            "data": {
                "_raw_search_results": [
                    {
                        "title": "Competitor Analysis: Evaluating Tesla And Competitors In Automobiles Industry - Benzinga",
                        "link": "https://news.google.com/rss/articles/CBMiygFBVV95cUxQeTBDVHYwMlVRRVNrZVdqTjQ0MlNOS0NvVEMwUlFRdjlDeFZ4UFBmR0I1Njl5M1pEQlJFNFNXWG9KZ0xfeVZELS1kR3JvY0xpT2JGSEpweFh3YkxqVVhHTHQ3UXB0TzQyLUhEN0RwejR1VE5DbEFZa1NVSmYxbG9iR3FCdVp5R2ItbGZmSHVlZDFRWGs1Y29aWGxZNVRqMlI0eHlnaEY1N3VlNkJzTjdFUEtkWUNpc3JoMHhndGJoSTYxNU1NT2NEMWl3?oc=5",
                        "published_date": "Fri, 19 Dec 2025 15:00:25 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Forbes Endorses Tesla FSD as Autonomy Leader Toward 2030 Dominance - WebProNews",
                        "link": "https://news.google.com/rss/articles/CBMimgFBVV95cUxNNWNMdkRIY2dUOW12Z1lLb2pxem1Zd1ZISkVMLVpmbXVTZGVqajE4djVDMXZwd3VmMnhleXZSV2hLZDFSU2d2cEVTbmwyWHZwLS10Wk1PNS15aTlmNmxReTVHNkgzeEhWMnhOYzg5M2E2MTgyWG1sRi1XdmRIbERQUTFXakNzQXNfY3ZHZGlTVWw5bHZhSTZtQ2N3?oc=5",
                        "published_date": "Mon, 22 Dec 2025 23:31:48 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Tesla's New Competitor Is a Huge Problem - Nasdaq",
                        "link": "https://news.google.com/rss/articles/CBMid0FVX3lxTFBTMURGenFLTE5qRjBhUlA2UFQ2cng5SG9lSFNxMlVpaDQtT3ZYNk5UTWNHSzU1VUdsbkxXanBGNHRmV19fUTI2OENNZ2NZT19yRlFkU1BJbGNwTHV4elhsX1FfNzEwQkp0TXBkTzBpMmhBcl96NDIw?oc=5",
                        "published_date": "Wed, 29 Oct 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Wikipedia: Tesla, Inc.",
                        "link": "https://en.wikipedia.org/wiki/Tesla,_Inc.",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Tesla, Inc. ( TEZ-lə or   TESS-lə) is an American multinational automotive and clean energy company."
                    },
                    {
                        "title": "Wikipedia: Tesla Autopilot",
                        "link": "https://en.wikipedia.org/wiki/Tesla_Autopilot",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Tesla Autopilot is an advanced driver-assistance system (ADAS) developed by Tesla, Inc. that provides partial vehicle automation, corresponding to Level 2 automation as defined by SAE International."
                    },
                    {
                        "title": "Wikipedia: Space launch market competition",
                        "link": "https://en.wikipedia.org/wiki/Space_launch_market_competition",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Space launch market competition is the manifestation of market forces in the launch service provider business. In particular it is the trend of competitive dynamics among payload transport capabilities at diverse prices having a greater influence on launch purchasing than the traditional political considerations of country of manufacture or the national entity using, regulating or licensing the launch service."
                    }
                ]
            },
            "summary": "Tesla competes with 0 major players with strong positioning in N/A segment.",
            "confidence": 1.0,
            "timestamp": "2025-12-24T16:35:25.522367"
        },
        {
            "research_type": "trends",
            "title": "Trends Analysis",
            "data": {
                "_raw_search_results": [
                    {
                        "title": "Tesla Stock Powers Ahead: Can TSLA Balance AI, EV Growth, and Net-Zero Goals? - CarbonCredits.com",
                        "link": "https://news.google.com/rss/articles/CBMiogFBVV95cUxQWW9qRWdweURmZkROVFg5N0RpTkJVMF85N2hyY3ltRk10SG9HSnhpNng0Z3NTZVp5R0dsQU1jTm84MU4xdlhyNXM1eV95Skw5WnFmSU1pQWtoUDhMekpFLXFHSmU0ckJJRk9jRFN4OUZlQTVGVms0MHVUSUNkRG9XdGNoUWRoR20xRmk0VHQxeDc1c2piYWlzdzI3SExfMURxa0E?oc=5",
                        "published_date": "Wed, 24 Sep 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Tesla News Today: Key Developments Influencing Tesla and Its Stock - vocal.media",
                        "link": "https://news.google.com/rss/articles/CBMilwFBVV95cUxONGZiMEhabmhQOU9JXzB5blBWcC1uMm5vNmNTaFVGSklsMjhTVUt3U1JJaEFOVmFRN3EwTV9BcGlkVFRNQ0ZrRGVPYlViMkl2eVQxaFNMRk9YWlB1MkZBNjhfSFZhQWZvSUxTZDYyMVI5QVkzbk1lMHRBZ2J2RVRPaE1GLWlHWURfb0hhR203LVdTMGx6WlRj?oc=5",
                        "published_date": "Thu, 18 Dec 2025 06:51:04 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Tesla's Market Rollercoaster: Navigating Innovation, Scrutiny, and Future Growth - FinancialContent",
                        "link": "https://news.google.com/rss/articles/CBMi5wFBVV95cUxOSWNVWWpZUFVlOUZTbmktN3R2UmJOWGVibEpTbUwwSllPSDJWWTNOWGVMMmF6TFZqdUhrNlUxV01pemRNeVA5RzNGdFhORG5mb0dKdTRmRUpjbjR3TnNMY2M1alItWmpuclFHeDFobmY4X25fR1VIY3MzV0pfRm9xckM1Y3JIb0otZWd6Q3dERkhheWRhdU1CVDdkLVhCUjNjaG0xUVdqejVYRXAzalUzUnpicXBiWDNXZmVEUmx1TkE5cUhUaV96SkExZldoS0JINGNCWVRLZjdhX0tYWkpLbEgtaVlqSjQ?oc=5",
                        "published_date": "Sun, 19 Oct 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Wikipedia: Tesla, Inc.",
                        "link": "https://en.wikipedia.org/wiki/Tesla,_Inc.",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Tesla, Inc. ( TEZ-lə or   TESS-lə) is an American multinational automotive and clean energy company."
                    },
                    {
                        "title": "Wikipedia: Internet of things",
                        "link": "https://en.wikipedia.org/wiki/Internet_of_things",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "The Internet of things (IoT) describes physical objects that are embedded with sensors, processing ability, software, and other technologies that connect and exchange data with other devices and systems over the Internet or other communication networks. The IoT encompasses electronics, communication, and computer science engineering."
                    },
                    {
                        "title": "Wikipedia: History of self-driving cars",
                        "link": "https://en.wikipedia.org/wiki/History_of_self-driving_cars",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "The history of self-driving cars began with experiments in radio-control during the 1920's, and the development of advanced driver assistance (ADAS) after WWII. Trials of self-driving vehicles began in the 1950s with the first semi-autonomous car developed in 1977 by Japan's Tsukuba Mechanical Engineering Laboratory. \nIn the United States, Carnegie Mellon University's Navlab began semi-autonomous vehicle projects in 1984, funded by the Defense Advanced Research Projects Agency (DARPA)."
                    }
                ]
            },
            "summary": "Tesla is positioned to benefit from trends in N/A with a N/A outlook.",
            "confidence": 1.0,
            "timestamp": "2025-12-24T16:35:33.023669"
        }
    ],
    "total_results": 10,
    "timestamp": "2025-12-24T16:35:33.038035",
    "report_id": "e6fd122f"
}