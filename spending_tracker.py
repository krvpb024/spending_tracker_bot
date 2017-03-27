if event.message.text == "記帳指令":
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=
        "查詢目前預算總額，請輸入：\n$目前預算\n\n重新設定預算為指定金額，請輸入：\ne.g.\n$設定預算 1000\n\n記帳請輸入金額及項目名稱\ne.g.\n$20 餅乾\n\n結算金額請輸入：\n$結算"
        )
    )


if re.match(r'^\w+\s\w+', event.message.text[1:]) and event.message.text.startswith("$設定預算") == False and event.message.text.startswith('$'):
    try:
        print('開始')
        int(event.message.text[1:].split()[0])

        print('更新總額')


        print('取得data')
        data = event.message.text[1:].split()
        print('完成')
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='確定新增項目？\n{} {}元'.format(data[1], data[0]),
                actions=[
                    PostbackTemplateAction(
                        label='確定',
                        text='確定',
                        data='addthing {} {} {}'.format(data[0], data[1], time.strftime("%Y/%m/%d", time.localtime()))
                    ),
                    MessageTemplateAction(
                        label='取消',
                        text='取消'
                        )
                    ]
                )
            )
        )
    except ValueError:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入正確格式\ne.g. $60 餅乾")
            )

if event.message.text.startswith('$'):
    sheet = get_gspread_auth()
    if event.message.text.startswith("$設定預算"):
        try:
            data = event.message.text.split()[1]
            int(data)

            sheet.update_cell('D1', data)
            sheet.update_cell('B1', data)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=
                "目前預算為：{}".format(sheet.get_value('B1'))
                )
            )
        except ValueError:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="預算只能為數字")
                )
        except IndexError:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請輸入數值作為預算")
                )
    elif sheet.get_value('B1') == "尚未設定":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=
            "目前尚無預算，請使用設定預算指令：\ne.g.\n$設定預算 1000\n\n即可使用記帳功能"
            )
        )
    else:
        if event.message.text.startswith("$目前預算"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=
                "目前預算為：{}".format(sheet.get_value('B1'))
                )
            )
        elif event.message.text == "$結算":
            all_amout = sheet.get_value('D1')
            after_amout = sheet.get_value('B1')
            last = int(sheet.get_value('D1')) - int(sheet.get_value('B1'))
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=
                "結算完畢\n原先預算：{}\n剩餘預算：{}\n總消費金額：{}".format(all_amout, after_amout, last))
                )
            sheet.update_cell('D3', all_amout)
            sheet.update_cell('E3', after_amout)
            sheet.update_cell('F3', last)
            sheet.update_cell('D1', '尚未設定')
            sheet.update_cell('B1', '尚未設定')
            sheet.insert_rows(row=2, values='')





    if event.postback.data.startswith("addthing"):
        data = event.postback.data.split() # ['addthing', '30', '餅乾', '2017/03/20']
        sheet = get_gspread_auth()
        new_amount = int(sheet.get_value('B1')) - int(data[1])
        print(new_amount)
        sheet.update_cell('B1', new_amount)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="新增消費項目：\n{}\n\n目前剩餘預算為：{}".format(data[2], sheet.get_value('B1')))
            )
        print('輸入項目')
        sheet.insert_rows(row=2, values=data[1:])
        print('完成')
