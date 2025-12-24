Request URL
http://localhost:8000/api/v1/research
Request Method
POST

{
  "entity_name": "Elon Musk",
  "entity_type": "individual",
  "research_types": [
    "financial",
    "sentiment",
    "news"
  ],
  "selected_providers": [
    "google_news",
    "linkedin",
    "wikipedia",
    "duckduckgo",
    "reddit",
    "github",
    "instagram",
    "youtube",
    "medium"
  ]
}

{
    "entity_name": "Elon Musk",
    "entity_type": "individual",
    "results": [
        {
            "research_type": "financial",
            "title": "Financial Analysis",
            "data": {
                "_raw_search_results": [
                    {
                        "title": "Elon Musk says “universal high income” is coming - thestreet.com",
                        "link": "https://news.google.com/rss/articles/CBMikwFBVV95cUxNcTJkM0prOGNDSnFSdmNkcHVSX0E2M014QmdFcDdVZG4zWnNuYVBCREUycklxb1cycDN5N1pleWxxc190aHNqRHU2SmdrZ1JLTDk3d2dOUXdSWVFLSW1ZWFRGUU5leVdDZGtQRFZmRGRLcjdqRkdYN3I2c0dDN3dmN2g2Rlpuelg1MFRYSGdndmtpSms?oc=5",
                        "published_date": "Thu, 18 Dec 2025 19:33:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "What Is Elon Musk's Net Worth? - moneywise.com",
                        "link": "https://news.google.com/rss/articles/CBMibkFVX3lxTE9DYkVrVjFadDZDNWJsZVVsZi15eTZvNzh5Z3E3dDFpeHRRZjVLU2MtQk5zdWh0LUJPVUdSb2l5SmI1TFo4WjJqM3lhamdZX1VzRmtPMVJKM0ozWGRFaUt3ZGNvTTlCOFdsQlNlLXVR?oc=5",
                        "published_date": "Fri, 23 May 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Nancy Pelosi to Retire in 2027: A Look at the Former Speaker’s Net Worth - Investopedia",
                        "link": "https://news.google.com/rss/articles/CBMibkFVX3lxTE82QThDVUZ4ZDZ3clhLTjdxeWdhSWRNVzRiaE5WcjhIbDF6OWdDZXNoQ01naDdHWFhCcUhUWGFoSXhkYzVLSkRNTERJblE5bmpYdkgxZVBvVmVIbUxreWM5Q0ZjVkY2NURPX0hobTlR?oc=5",
                        "published_date": "Fri, 07 Nov 2025 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Wikipedia: OpenAI",
                        "link": "https://en.wikipedia.org/wiki/OpenAI",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "OpenAI is an American artificial intelligence (AI) organization headquartered in San Francisco, California. It aims to develop \"safe and beneficial\" artificial general intelligence (AGI), which it defines as \"highly autonomous systems that outperform humans at most economically valuable work\"."
                    },
                    {
                        "title": "Wikipedia: Department of Government Efficiency",
                        "link": "https://en.wikipedia.org/wiki/Department_of_Government_Efficiency",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "The Department of Government Efficiency (DOGE) was an initiative by the second Trump administration in the United States. Its stated objective was to modernize information technology, maximize productivity, and cut excess regulations and spending within the federal government."
                    },
                    {
                        "title": "Wikipedia: Nikhil Kamath",
                        "link": "https://en.wikipedia.org/wiki/Nikhil_Kamath",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Nikhil Kamath (born 5 September 1986) is an Indian entrepreneur and investor. He is the co-founder of Zerodha, a retail stockbroker, and True Beacon, an asset management company."
                    }
                ]
            },
            "summary": "Analysis completed for Elon Musk",
            "confidence": 1.0,
            "timestamp": "2025-12-24T16:38:08.787347"
        },
        {
            "research_type": "sentiment",
            "title": "Sentiment Analysis",
            "data": {
                "_raw_search_results": [
                    {
                        "title": "Is Elon Musk’s DOGE ‘very popular’? That’s not what the polls say - Poynter",
                        "link": "https://news.google.com/rss/articles/CBMikwFBVV95cUxQbmhjaTdmaDE2bEw0VFF4WENSX0thcTZxeVdBRkl1NkJCQm5MNHNoOVgzZ2xHRjlIMS1kbnBabUlCSEpqU2h2SVRfeUFOb3kzbklzWUVzU2F5Nk1fMW9zQWlxS2FJVkVtRy1SZ0FQMjBKc1FsUmdubzJUbTJGLUhwY2JMUlpqRl9ocnhQVWx3N2VnUHc?oc=5",
                        "published_date": "Mon, 10 Mar 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Thanks, Elon—It Sure Is Weird Being a Tesla Owner Right Now - MotorTrend",
                        "link": "https://news.google.com/rss/articles/CBMixAFBVV95cUxNWENKdjFYSHpQWDd6YTBsbmJST1RFMmtrRXJ6SUswZ05oSEpoUVZaUkFpcXBNU3JES0l1NVhscThQMHZTRUlETGI4cTR5VGd1Z0d5ZzBJWWtHVVdhTXA2R012bzFCUWZTNXpZSXhYOFI4UHJUekh0VGxTR3NuTE5hMnFOdVZydjg5MmJKZ0xSMG9aQWNiYjZIMHE5dGV4ZFR6dUpUUTVnMmhZQUVtUFpNX2h6ZDA2aTBxNEJjaVN5Q29tWTlI?oc=5",
                        "published_date": "Thu, 03 Apr 2025 07:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "How Americans view Elon Musk and Mark Zuckerberg - Pew Research Center",
                        "link": "https://news.google.com/rss/articles/CBMiogFBVV95cUxOUFJKMzlxd3Q0X1FiMHNyVjdrRWw5Zi1zR1JWckU3OUc3VW81VXVSOFZ5MlIxUkM5UHhEMTd3ak4yZVFlX19DWmpVRHJYZHIxMHdYaVNyZlJ6eW1id2c0MjVGb1ZRQTVIZzBuMldkUW9fMUhmOWYyZVduOERHb0EtVVlRbzlVWHVvZjZfbGhlaDJwQkpFNC13d0dLZFM5a0psR3c?oc=5",
                        "published_date": "Wed, 19 Feb 2025 08:00:00 GMT",
                        "source": "Google News"
                    },
                    {
                        "title": "Wikipedia: Twitter use by Donald Trump",
                        "link": "https://en.wikipedia.org/wiki/Twitter_use_by_Donald_Trump",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Donald Trump's use of social media attracted worldwide attention since he joined Twitter in May 2009. Over nearly twelve years, Trump tweeted around 57,000 times, including about 8,000 times during the 2016 election campaign and over 25,000 times during his first presidency."
                    },
                    {
                        "title": "Wikipedia: Batya Ungar-Sargon",
                        "link": "https://en.wikipedia.org/wiki/Batya_Ungar-Sargon",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Batya Ungar-Sargon is an American journalist and author who served as the opinion editor of The Forward and later worked as deputy opinion editor of Newsweek. She is the author of two books, which address class consciousness and working class-related issues."
                    },
                    {
                        "title": "Wikipedia: Second presidency of Donald Trump",
                        "link": "https://en.wikipedia.org/wiki/Second_presidency_of_Donald_Trump",
                        "published_date": "",
                        "source": "Wikipedia",
                        "snippet": "Donald Trump's second and current tenure as the president of the United States began upon his inauguration as the 47th president on January 20, 2025. Trump, a member of the Republican Party, had previously served as the 45th president from 2017 to 2021 and lost re-election to the Democratic nominee Joe Biden in the 2020 presidential election, took office after defeating the Democratic incumbent vice president Kamala Harris in the 2024 presidential election."
                    }
                ]
            },
            "summary": "Analysis completed for Elon Musk",
            "confidence": 1.0,
            "timestamp": "2025-12-24T16:38:22.566192"
        },
        {
            "research_type": "news",
            "title": "News Analysis",
            "data": {
                "recent_news": [
                    {
                        "headline": "Elon Musk, AI and the antichrist: the biggest tech stories of 2025 - The Guardian",
                        "date": "Tue, 23 Dec 2025 19:22:00 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMiggFBVV95cUxOTnhaUURYZ2laU3hMYXl6a3Y0N2pXSm80UGs4dmEzVVd2RzJVWnBoRkhvdnUxUjZTMWpSemE2R2R0M0pvMGNLOVJDOXFBUUpkWjZDdWtKdURBMHplbndSQ3E1LVREdXYyMGRkdV9WSVFFbE02OVVBWjZNd3pxdXN4VFF3?oc=5"
                    },
                    {
                        "headline": "Elon Musk Demanded Tesla’s Electric Doors Despite Safety Worries - Bloomberg.com",
                        "date": "Mon, 22 Dec 2025 22:00:08 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMirgFBVV95cUxQQi1PLUlLUlAtazgxenprcFF0Um9FZ2lGbkJvblRwQ2ZpY000VnJMeUp6eDZ6MXpCbzl2bFFYeEFMOU1GTFNQVXA0TDVLckdtVlU4WEUtbWh6MGxzUjdlemRBYzhXUzNQV1JRRkZkdS1nblBYT3BlbjVLYndMalZVWGl6alZNYUVtUGRiS1g0dkF6dTB1X2lTQXAzcU9vdk04cFJBeTVUcDNpZTJIZ1E?oc=5"
                    },
                    {
                        "headline": "Elon Musk calls Columbus Mayor Andrew Ginther a 'traitor to America' - The Columbus Dispatch",
                        "date": "Mon, 22 Dec 2025 19:55:00 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMi8AFBVV95cUxNMzhOdWtMU05yaUQ2OGJqei1iOHhNYXQ1cmZfMVpZNDVBb3kxQWFlRXJnQy1JYVRUWWl6TjQ0Y2JxUzFaVkExM1ctSDRQRU9zWWxfTUZVZEkwYzRnN2wwdzVFUGlWYTN2QXlDY0pMMGFNVm5iYllIU2s5Q2xFQktOMTc1bGw5MDZjQk1KelBVSGQ5cE05SjRaa04tcVp0Z2tRRThDd1lhZmRZUmZ4QnVRaDhHbHVTYUtYbVZiNl8zRE1ETzcyd19xWTYwZjM2ak1tUng1WGtaRHZXVXZQd3pFNThkNGticW5pRmtrNXptQ2w?oc=5"
                    },
                    {
                        "headline": "Starlink in the crosshairs: How Russia could attack Elon Musk's conquering of space - ABC News",
                        "date": "Mon, 22 Dec 2025 07:47:29 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMitgFBVV95cUxQbVp6WHVCUzVsNHVTMnBWenRiakhKTGM2OUQyNzRXbEFWQU5QM0d6anFrZGJOeGM3cV9WUU43QnVvVDJLMmc1TzE3NDdsdzBHZzROMWdxLWo4Q3JvUm9ZOF9vY3J2bjR2NU9mNGpSUGVpUmJYbEtTVjJQZTYtT1dTMVo2Rl9PVnFDNjhubk9JSVhaWTEwSXBtekQ2RTB2T2Y5dVo1aEo5SlZwdDZqSTJaa3lDUUg2d9IBuwFBVV95cUxOSlJ3Qms1aTVrYTZQUjlfLWxKcmdieVVpWUdnbmJ2amRGSzNoOUpXZm1oYXVvQ3NtYzFxcnA0d2JpQy1qdVVVRXA0MGJkR2JHdDJsaHZ6Rzc0Z1lYS3daZW1aSlM3THJaU3hBMDVNaC1oZzktZ0xoa0hzNW84TS1oTnliTTJpQTNSc3J4dnlTSVBFaElCUE1uOTZWT1V4dWNYcnFGdW5lSUlrVTd2X1BBeUVaTGdia0dFM180?oc=5"
                    },
                    {
                        "headline": "Elon Musk adds to his $679 billion fortune after Delaware court reverses its earlier decision and awards him a $55 billion Tesla pay package - Fortune",
                        "date": "Sun, 21 Dec 2025 00:25:00 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMitgFBVV95cUxPUkFqTXRpbm5BRnBLVDRmUUwyMDFMU3RTUHVjempCSXk1bTEzUWtKdTVFcHd1QzJqT2piWnl1OFQ1amFQQ3JaNFJxVnBaTzRXVjM0QzM3WE9EUnd6QVY0T2h1UWxSMWZnYU5ObmJqRERTR25aX0tfbUJiRVd5dVkxUzRleG9qMHdTWjY4UHJ3UkJkb3I5NDFZQUFGYnA3VnE0WGJ0TDdqbmhSTlJmX0pkdWUyenhTdw?oc=5"
                    },
                    {
                        "headline": "Readers always tell me I'm wrong, but I was right about Trump | Opinion - USA Today",
                        "date": "Tue, 23 Dec 2025 19:35:00 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMiqgFBVV95cUxNZ0JXa0Y4SUgyZXBINllvaE42amI2UGVwVDRfRGxpbF9OakNRdzU0dzFVTjlhQXRKcFMzLUt2RF84bU1NVEtqUnZLMWhxcjNZOGJJT0YyVTJwYVZqTXNLSFRndV9XNC1RRXZFWUNaMGJZQmxLMk5VNHNiVjB1SW9PbGEzMUJ2cjNZRjhuZ1RqMk83WnQtdWw2WmlxdlpHbHFRTXN1ckxXejBUUQ?oc=5"
                    },
                    {
                        "headline": "How Did DOGE Disrupt So Much While Saving So Little? - The New York Times",
                        "date": "Wed, 24 Dec 2025 00:27:30 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMiggFBVV95cUxNbzB4WVdjVFBJMlREQXVOR3JYampuaFVmbENySG9kMGFTV0dOUU5JVmNhVFptcnc0Z1YwNTkwMy04MHN5Mk5SVEtBTkxJSkFXLUZyd3VJcVFsUDJmcklPQ0VBblNHUnhLTUYzeGVRbHNxeWVveTdtNUxzSnM0OUJJNWJn?oc=5"
                    },
                    {
                        "headline": "Elon Musk's Starlink is adding 20,000 new users a day as it hits 9 million customers - Business Insider",
                        "date": "Tue, 23 Dec 2025 11:51:00 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMipAFBVV95cUxOTTd6TGlFOG9LZmVKWklLLXE2WTRaSVV3eTBFemlzVDlNLUhhYkxVX05VVFFjWURGSFZtYUFqbnNYVHBUbi1BTEl0N3VUX0Q3X29GVWs1TVRfSWVTakVieGJXd3duVVlnYXV5SkR4Znh4SDEtNWZmMWlzSGpNazh2dy1oUEZkVkdXMXNMTC0tVDk4MWc0R2tnUjZzdGRPcC16Vk9XaQ?oc=5"
                    },
                    {
                        "headline": "‘The True Currency’—$750 Billion Tesla CEO Elon Musk Sparks Wild Bitcoin Speculation Amid ‘Infinite Money Glitch’ Debate - Forbes",
                        "date": "Sun, 21 Dec 2025 12:51:43 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMigAJBVV95cUxOODdWQ2NUd0pOZFZCTU81S3RkNm9fLVRxNHdoZHcxdDRWQkZMOFVINmdST1QwLWlIVVF1NTA0WktSbG1ORTNyTUx4T1poaVlEZGFtcVJNUlg5VTRBRkp6V2RGcDJWZFZHV1lNWms4U01ibWNtWkpqUEw3LWpvdXpjWE52Ql9ucHNWbFc0Nk9FRTl5bXhsU1Y4U2pSNXh3LVR0V0FuVkZ3VVpGUlBvVmRsWi1oeXMza1l0cG5tdzR4Rkc4ZEtPb2Q3THNoTVZtZ3l3NmF4Q01ES0lFZXdvZUNRTUNPUjl5OEtycmVMbGxCZUhyQUNuSldnaGpSLTlQZmNo?oc=5"
                    },
                    {
                        "headline": "Elon Musk's ex-wife Talulah Riley remembers one simple line Tesla CEO told her on Christmas: I just wante - Times of India",
                        "date": "Wed, 24 Dec 2025 10:27:00 GMT",
                        "source": "Google News",
                        "link": "https://news.google.com/rss/articles/CBMiogJBVV95cUxNTVdrRmNSZmJ4Z0Q0UmE2ZHpGWVlXUHhjV1FvQ3RTSE5jV0J3MkFsQ01EdV8wVHZYa001a3NBY05zclU4QTBxUW15dGdYUzF3bkRiSDA3dVkwUkhfVWplcHN5YWt2UDBzbXlwYUUyNURCRlZGd21nSS1MZWNxUWpVTFJvY3p0TzhqWkFFRHFnRzhzeDRPdDZocG1xSGtBRjg1blZMUG1hTFpyWENHb21WUlF5R2dUbGRwWF9rOUF1V0lRZWhSa1BCYkM4allwcmVfRWxHNWt5ZzJ4NkhuNnRFQkxOSmxlRk5qNmd3Mng2YkE5bERSSWJjTGkzMU5SS2xTRFlHRmNuMWdhVzk0UW5qQXBUcmVhQkcwREM5WXJ6TXJ5Z9IBpwJBVV95cUxPSEdRdnRYTTFZeTFXaTVwSEJHT2xhOThiRVJ4LXJNZWRCellKNnQ0eS1vUWRFNWR2RVNKNURQY2lSNFVQNF85SlJiaTl6NldCYkd6aS1QdHhaeHV4Qms3bjFuVDl0T1l1YWFGLWV0TGMxdGNQSHNVNGhMMWVrTEVMT3hnU0dIV1NSeDNNTWliRGNKTFhBeU9jWkNyQTlmWE16Q2VfbEd5Ym9hVjI3Q0NsVFl1SXB3a3VzNWdPNDRSMVk3bEgyVzJjMDdHM0tRMVBzdzlwYnNnNEEtcVBPaTVXTURuWkNHT29kb2R6TnFvcGgyS0pDNElMYUZ4VUtKcEwxUkc0dlN5cURTM0paVHRmcTVjdXpIUUhucFN2cVR0Z0F5bE8wS1dF?oc=5"
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
            "summary": "Elon Musk has 10 recent articles analyzed.",
            "confidence": 0.5,
            "timestamp": "2025-12-24T16:38:23.366952"
        }
    ],
    "total_results": 3,
    "timestamp": "2025-12-24T16:38:23.375652",
    "report_id": "f662065c"
}