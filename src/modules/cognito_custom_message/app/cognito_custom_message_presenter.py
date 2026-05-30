def lambda_handler(event, context):
    trigger_source = event.get('triggerSource')
    
    if trigger_source in ['CustomMessage_SignUp', 'CustomMessage_ResendCode']:
        code = event['request']['codeParameter']
        event['response']['emailSubject'] = "Bem vindo ao sistema de autenticação Nutri Esportiva São Camilo"
        event['response']['emailMessage'] = f"Olá!<br><br>Obrigado por se registrar no Nutri Esportiva São Camilo.<br><br>O código para verificar seu e-mail e ativar sua conta é: <b>{code}</b><br><br>Se você não se registrou no Nutri Esportiva São Camilo, por favor ignore este e-mail."
    
    elif trigger_source == 'CustomMessage_ForgotPassword':
        code = event['request']['codeParameter']
        event['response']['emailSubject'] = "Recuperação de Senha - Nutri Esportiva São Camilo"
        event['response']['emailMessage'] = f"Olá,<br><br>Você solicitou a recuperação de senha da sua conta.<br><br>Seu código de verificação é: <b>{code}</b><br><br>Se você não solicitou esta alteração, ignore este e-mail."
        
    return event
