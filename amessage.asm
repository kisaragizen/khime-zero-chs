mov esi,eax
mov edi,khime_zero_chs.45B8B0
sub esp,10
lodsb
cmp al,byte ptr ds:[edi]
jne khime_zero_chs.45214C
test al,al
je khime_zero_chs.452129
inc edi
jmp khime_zero_chs.45211D
add esp,10
push 40
push khime_zero_chs.45B840
push khime_zero_chs.45B850
push 0
call dword ptr ds:[<MessageBoxA>]
popad
call dword ptr ds:[<CreateFileA>]
jmp khime_zero_chs.4228E5
add esp,10
popad
call dword ptr ds:[<CreateFileA>]
jmp khime_zero_chs.4228E5