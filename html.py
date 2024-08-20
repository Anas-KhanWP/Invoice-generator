html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Invoice</title>
                <style>
                    * {{
                        border: 0;
                        box-sizing: content-box;
                        color: inherit;
                        font-family: inherit;
                        font-size: inherit;
                        font-style: inherit;
                        font-weight: inherit;
                        line-height: inherit;
                        list-style: none;
                        margin: 0;
                        padding: 0;
                        text-decoration: none;
                        vertical-align: top;
                    }}

                    address {{
                        display: flex;
                        flex-direction: row;
                        flex-wrap: wrap;
                        align-content: center;
                        justify-content: space-between;
                    }}
                    *[contenteditable] {{ border-radius: 0.25em; min-width: 1em; outline: 0; }}

                    *[contenteditable] {{ cursor: pointer; margin-bottom: 0; }}

                    *[contenteditable]:hover, *[contenteditable]:focus, td:hover *[contenteditable], td:focus *[contenteditable], img.hover {{ background: #DEF; box-shadow: 0 0 1em 0.5em #DEF; }}

                    span[contenteditable] {{ display: inline-block; }}

                    /* heading */

                    h1 {{ font: bold 100% sans-serif; letter-spacing: 0.5em; text-align: center; text-transform: uppercase; }}

                    /* table */

                    table {{ font-size: 75%; table-layout: fixed; width: 100%; }}
                    table {{ border-collapse: separate; border-spacing: 2px; }}
                    th, td {{ border-width: 1px; padding: 0.5em; position: relative; text-align: left; }}
                    th, td {{ border-radius: 0.25em; border-style: solid; }}
                    th {{ background: #EEE; border-color: #BBB; }}
                    td {{ border-color: #DDD; }}

                    /* page */

                    html {{ font: 16px/1 'Open Sans', sans-serif; overflow: auto; padding: 0.5in; }}
                    html {{ background: #999; cursor: default; }}

                    body {{ box-sizing: border-box; height: 11in; margin: 0 auto; overflow: hidden; padding: 0.5in; width: 8.5in; }}
                    body {{ background: #FFF; border-radius: 1px; box-shadow: 0 0 1in -0.25in rgba(0, 0, 0, 0.5); }}

                    /* header */

                    header {{ margin: 0 0 3em; }}
                    header:after {{ clear: both; content: ""; display: table; }}

                    header h1 {{ background: #000; border-radius: 0.25em; color: #FFF; margin: 0 0 1em; padding: 0.5em 0; }}
                    header address {{ float: left; font-size: 75%; font-style: normal; line-height: 1.25; margin: 0 1em 1em 0; }}
                    header address p {{ margin: 0 0 0.25em; }}
                    header span, header img {{ display: block; float: left; }}
                    header span {{ margin: 0 0 1em 1em; max-height: 25%; max-width: 60%; position: relative; }}
                    header img {{ max-height: 100%; max-width: 100%; }}
                    header input {{ cursor: pointer; -ms-filter:"progid:DXImageTransform.Microsoft.Alpha(Opacity=0)"; height: 100%; left: 0; opacity: 0; position: absolute; top: 0; width: 100%; }}

                    /* article */

                    article, article address, table.meta, table.inventory {{ margin: 0 0 3em; }}
                    article:after {{ clear: both; content: ""; display: table; }}
                    article h1 {{ clip: rect(0 0 0 0); position: absolute; }}

                    article address {{ float: left; font-size: 125%; font-weight: bold; margin: 0; }}
                    article address table {{ margin: 0 0 10px 0 !important; }}
                    article {{ margin-bottom: 15px; }}
                    
                    header {{ margin: 0 0 1.2em 0; }}

                    /* table meta & balance */

                    #meta1 {{
                        z-index: 9;
                        opacity: 1;
                    }}

                    .smeta td {{
                        width: 60%;
                    }}
                    .smeta {{
                        float: right;
                        width: 40%;
                    }}

                    table.meta, table.balance {{
                        float: right;
                        width: 40%;
                    }}
                    table.meta:after, table.balance:after {{ clear: both; content: ""; display: table; }}

                    /* table meta */

                    table.meta th {{
                        width: 58%;
                    }}
                    table.meta td {{ width: 60%; }}

                    /* table items */

                    table.inventory {{ clear: both; width: 100%; }}
                    table.inventory th {{ font-weight: bold; text-align: center; }}

                    table.inventory td:nth-child(1) {{ width: 26%; }}
                    table.inventory td:nth-child(2) {{ width: 38%; }}
                    table.inventory td:nth-child(3) {{ text-align: right; width: 12%; }}
                    table.inventory td:nth-child(4) {{ text-align: right; width: 12%; }}
                    table.inventory td:nth-child(5) {{ text-align: right; width: 12%; }}

                    /* table balance */

                    table.balance th, table.balance td {{ width: 50%; }}
                    table.balance td {{ text-align: right; }}

                    /* aside */

                    aside h1 {{ border: none; border-width: 0 0 1px; margin: 0 0 1em; }}
                    aside h1 {{ border-color: #999; border-bottom-style: solid; }}

                    /* javascript */

                    .add, .cut {{
                        border-width: 1px;
                        display: block;
                        font-size: .8rem;
                        padding: 0.25em 0.5em;	
                        float: left;
                        text-align: center;
                        width: 0.6em;
                    }}

                    .add, .cut {{
                        background: #9AF;
                        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
                        background-image: -moz-linear-gradient(#00ADEE 5%, #0078A5 100%);
                        background-image: -webkit-linear-gradient(#00ADEE 5%, #0078A5 100%);
                        border-radius: 0.5em;
                        border-color: #0076A3;
                        color: #FFF;
                        cursor: pointer;
                        font-weight: bold;
                        text-shadow: 0 -1px 2px rgba(0,0,0,0.333);
                    }}

                    .add {{ margin: -2.5em 0 0; }}

                    .add:hover {{ background: #00ADEE; }}

                    .cut {{ opacity: 0; position: absolute; top: 0; left: -1.5em; }}
                    .cut {{ -webkit-transition: opacity 100ms ease-in; }}

                    tr:hover .cut {{ opacity: 1; }}

                    @media print {{
                        * {{ -webkit-print-color-adjust: exact; }}
                        html {{ background: none; padding: 0; }}
                        body {{ box-shadow: none; margin: 0; }}
                        span:empty {{ display: none; }}
                        .add, .cut {{ display: none; }}
                    }}

                    @page {{ margin: 0; }}
                </style>
            </head>
            <body>
                <header>
                    <h1>Invoice</h1>
                    <img width="180" height="130" alt="Logo" src="data:image/png;base64,{logo_base64}">
                    <table class="smeta">
                        <tr>
                            <th>Invoice #</th>
                            <td>{invoice_number}</td>
                        </tr>
                        <tr>
                            <th>Date</th>
                            <td>{invoice_date}</td>
                        </tr>
                        <tr>
                            <th>Venue</th>
                            <td>{venue}</td>
                        </tr>
                    </table>
                </header>
                <article>
                    <h1>Recipient</h1>
                    <address>
                        <table class="meta" id="meta1">
                            <tr>
                                <th>Client Name</th>
                                <td>{client_name}</td>
                            </tr>
                            <tr>
                                <th>Phone Number</th>
                                <td>{phone_number}</td>
                            </tr>
                            <tr>
                                <th>Bill To</th>
                                <td>{bill_to}</td>
                            </tr>
                        </table>
                        <table class="meta" style="width: 50%;">
                            <tr>
                                <th style="width: 40%;"><span contenteditable>Bank</span></th>
                                <td><span contenteditable>HBL (Habib Bank Limited)</span></td>
                            </tr>
                            <tr>
                                <th style="width: 40%;"><span>Account Title</span></th>
                                <td><span>Rameez Ahmed</span></td>
                            </tr>
                            <tr>
                                <th style="width: 40%;"><span>Account Number</span></th>
                                <td><span></span><span>00207901029503</span></td>
                            </tr>
                        </table>
                    </address>
                    <section style="overflow: auto;border: 1px solid;">
                        <table class="inventory">
                            <thead>
                                <tr>
                                    <th>Item</th>
                                    <th>Description</th>
                                    <th>Rate</th>
                                    <th>Quantity</th>
                                    <th>Price</th>
                                </tr>
                            </thead>
                            <tbody>
                                {item_rows}
                            </tbody>
                        </table>
                        <table class="balance">
                            <tr>
                                <th>Total</th>
                                <td>{total_amount:.2f}</td>
                            </tr>
                            <tr>
                                <th>Amount Paid</th>
                                <td>{amount_paid:.2f}</td>
                            </tr>
                            <tr>
                                <th>Balance Due</th>
                                <td>{balance_due:.2f}</td>
                            </tr>
                        </table>
                    </section>
                </article>
                <aside>
                    <h1><span contenteditable>Additional Notes</span></h1>
                    <div contenteditable>
                        <p>
                        <h3 style="font-weight: 600;">Payment Terms:</h3><br />
                        <ul>
                            <li class="__lis"><span>A 50% advance will be given before the event, and the remaining
                                    payment will be cleared by the next day of the event. Otherwise, raw data will not be provided
                                    for selection.</span></li>
                        </ul><br />
                        <h3 style="font-weight: 600;">Terms and Conditions:</h3><br />
                        <ul>
                            <li class="__lis">No payment will be refunded in case of any mishap or unforeseen situation /
                                circumstances occurred.</li> <br />
                            <li class="__lis">Client can only provide the extended date of the event.</li> <br />
                            <li class="__lis">Misbehavior of client will not be accepted.</li> <br />
                            <li class="__lis">If photographer provides any suggestion / advice regarding event management and client
                                don't listen or take it seriously so it will be not our responsibility.</li><br />
                            <li class="__lis">Client Pictures will be used on our page regarding marketing purposes at Instagram and
                                Facebook.</li><br />
                            <li class="__lis">Ask for update on editing after 15 days of the event.</li><br />
                        </ul>
                        </p>
                        <p>Kindly read this E-mail and instructions carefully and reply back to this but E-mail for confirmation. If
                            any query so please contact us on:</p><br />

                        <div style="display: flex;
                        flex-direction: column;
                        flex-wrap: wrap;
                        align-content: flex-end;
                        margin-top: 10px;">
                            <div>
                                <h4 style="font-weight: 600; font-size: 1.1rem;">Thanks & Regards,</h4>
                            </div><br />
                            <span style="font-size: 1.1rem;">Team Rameezdesaiphotography</span>
                            .
                        </div>
                    </div>
                </aside>
            </body>
            </html>
            """