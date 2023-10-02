import comfy .options #line:1
comfy .options .enable_args_parsing ()#line:2
import os #line:4
import importlib .util #line:5
import folder_paths #line:6
import time #line:7
def execute_prestartup_script ():#line:9
    def OOOO00OO0OO000O0O (O0OOOOO0OOOO0OOOO ):#line:10
        O0OOO000OOO000OO0 =os .path .splitext (O0OOOOO0OOOO0OOOO )[0 ]#line:11
        try :#line:12
            OO0OO000OO00OOOO0 =importlib .util .spec_from_file_location (O0OOO000OOO000OO0 ,O0OOOOO0OOOO0OOOO )#line:13
            OO000OOO0000OO0OO =importlib .util .module_from_spec (OO0OO000OO00OOOO0 )#line:14
            OO0OO000OO00OOOO0 .loader .exec_module (OO000OOO0000OO0OO )#line:15
            return True #line:16
        except Exception as OO00O0OOO0O0O0000 :#line:17
            print (f"Failed to execute startup-script: {O0OOOOO0OOOO0OOOO} / {OO00O0OOO0O0O0000}")#line:18
        return False #line:19
    O000OO000OO0OOO00 =folder_paths .get_folder_paths ("custom_nodes")#line:21
    for OO00OO00O0OOO0OOO in O000OO000OO0OOO00 :#line:22
        OO0000O0OO000OO0O =os .listdir (OO00OO00O0OOO0OOO )#line:23
        OOO0000O0OOOO000O =[]#line:24
        for OO000O0OO0O0O0O00 in OO0000O0OO000OO0O :#line:26
            O000OO0000OO00OOO =os .path .join (OO00OO00O0OOO0OOO ,OO000O0OO0O0O0O00 )#line:27
            if os .path .isfile (O000OO0000OO00OOO )or O000OO0000OO00OOO .endswith (".disabled")or O000OO0000OO00OOO =="__pycache__":#line:28
                continue #line:29
            O0O0OOO0OO0OOOOOO =os .path .join (O000OO0000OO00OOO ,"prestartup_script.py")#line:31
            if os .path .exists (O0O0OOO0OO0OOOOOO ):#line:32
                OO00O0OOO0O000O0O =time .perf_counter ()#line:33
                O0O00OO0OO0OOO00O =OOOO00OO0OO000O0O (O0O0OOO0OO0OOOOOO )#line:34
                OOO0000O0OOOO000O .append ((time .perf_counter ()-OO00O0OOO0O000O0O ,O000OO0000OO00OOO ,O0O00OO0OO0OOO00O ))#line:35
    if len (OOO0000O0OOOO000O )>0 :#line:36
        print ("\nPrestartup times for custom nodes:")#line:37
        for OO00OO00OO0OO0000 in sorted (OOO0000O0OOOO000O ):#line:38
            if OO00OO00OO0OO0000 [2 ]:#line:39
                OO000OO00OO0O00OO =""#line:40
            else :#line:41
                OO000OO00OO0O00OO =" (PRESTARTUP FAILED)"#line:42
            print ("{:6.1f} seconds{}:".format (OO00OO00OO0OO0000 [0 ],OO000OO00OO0O00OO ),OO00OO00OO0OO0000 [1 ])#line:43
        print ()#line:44
execute_prestartup_script ()#line:46
import asyncio #line:50
import itertools #line:51
import shutil #line:52
import threading #line:53
import gc #line:54
from comfy .cli_args import args #line:56
if os .name =="nt":#line:58
    import logging #line:59
    logging .getLogger ("xformers").addFilter (lambda OO0OOO000O00OOOO0 :'A matching Triton is not available'not in OO0OOO000O00OOOO0 .getMessage ())#line:60
if __name__ =="__main__":#line:62
    if args .cuda_device is not None :#line:63
        os .environ ['CUDA_VISIBLE_DEVICES']=str (args .cuda_device )#line:64
        print ("Set cuda device to:",args .cuda_device )#line:65
    import cuda_malloc #line:67
import comfy .utils #line:69
import yaml #line:70
import execution #line:72
import server #line:73
from server import BinaryEventTypes #line:74
from nodes import init_custom_nodes #line:75
import comfy .model_management #line:76
def cuda_malloc_warning ():#line:78
    OO0OO0OOO0O00000O =comfy .model_management .get_torch_device ()#line:79
    O0OO0OO0O00000OO0 =comfy .model_management .get_torch_device_name (OO0OO0OOO0O00000O )#line:80
    OOO0OOO0O0OOO000O =False #line:81
    if "cudaMallocAsync"in O0OO0OO0O00000OO0 :#line:82
        for O000O000OO0O0O00O in cuda_malloc .blacklist :#line:83
            if O000O000OO0O0O00O in O0OO0OO0O00000OO0 :#line:84
                OOO0OOO0O0OOO000O =True #line:85
        if OOO0OOO0O0OOO000O :#line:86
            print ("\nWARNING: this card most likely does not support cuda-malloc, if you get \"CUDA error\" please run ComfyUI with: --disable-cuda-malloc\n")#line:87
def prompt_worker (O000O0000OOO0O0OO ,O0000OO00OOO000O0 ):#line:89
    OO00000O0O00000O0 =execution .PromptExecutor (O0000OO00OOO000O0 )#line:90
    while True :#line:91
        OOOO000O0O00OOO00 ,OOO00OO00000O000O =O000O0000OOO0O0OO .get ()#line:92
        O0O000000000OO0O0 =time .perf_counter ()#line:93
        OOO00OO000O0OO00O =OOOO000O0O00OOO00 [1 ]#line:94
        OO00000O0O00000O0 .execute (OOOO000O0O00OOO00 [2 ],OOO00OO000O0OO00O ,OOOO000O0O00OOO00 [3 ],OOOO000O0O00OOO00 [4 ])#line:95
        O000O0000OOO0O0OO .task_done (OOO00OO00000O000O ,OO00000O0O00000O0 .outputs_ui )#line:96
        if O0000OO00OOO000O0 .client_id is not None :#line:97
            O0000OO00OOO000O0 .send_sync ("executing",{"node":None ,"prompt_id":OOO00OO000O0OO00O },O0000OO00OOO000O0 .client_id )#line:98
        print ("Prompt executed in {:.2f} seconds".format (time .perf_counter ()-O0O000000000OO0O0 ))#line:100
        gc .collect ()#line:101
        comfy .model_management .soft_empty_cache ()#line:102
async def run (OOOO0O0O00000000O ,address ='',port =8188 ,verbose =True ,call_on_start =None ):#line:104
    await asyncio .gather (OOOO0O0O00000000O .start (address ,port ,verbose ,call_on_start ),OOOO0O0O00000000O .publish_loop ())#line:105
def hijack_progress (O0OO0000000O0O00O ):#line:108
    def O0OOOOOO0O0O0O0O0 (O0OO00O000O000O0O ,O000000000O0OOOOO ,O0OOOOOO0O0OOOOO0 ):#line:109
        comfy .model_management .throw_exception_if_processing_interrupted ()#line:110
        O0OO0000000O0O00O .send_sync ("progress",{"value":O0OO00O000O000O0O ,"max":O000000000O0OOOOO },O0OO0000000O0O00O .client_id )#line:111
        if O0OOOOOO0O0OOOOO0 is not None :#line:112
            O0OO0000000O0O00O .send_sync (BinaryEventTypes .UNENCODED_PREVIEW_IMAGE ,O0OOOOOO0O0OOOOO0 ,O0OO0000000O0O00O .client_id )#line:113
    comfy .utils .set_progress_bar_global_hook (O0OOOOOO0O0O0O0O0 )#line:114
def cleanup_temp ():#line:117
    O000000OOO0O00OOO =folder_paths .get_temp_directory ()#line:118
    if os .path .exists (O000000OOO0O00OOO ):#line:119
        shutil .rmtree (O000000OOO0O00OOO ,ignore_errors =True )#line:120
def load_extra_path_config (O0O0OOO0OOOO00O0O ):#line:123
    with open (O0O0OOO0OOOO00O0O ,'r')as OO0000OOOOOO0OO00 :#line:124
        O0OO0000O0O0OO0O0 =yaml .safe_load (OO0000OOOOOO0OO00 )#line:125
    for O0O00O0O00OOO0O00 in O0OO0000O0O0OO0O0 :#line:126
        O00O00O0OOO0000O0 =O0OO0000O0O0OO0O0 [O0O00O0O00OOO0O00 ]#line:127
        if O00O00O0OOO0000O0 is None :#line:128
            continue #line:129
        O0000OOO00OOOOOOO =None #line:130
        if "base_path"in O00O00O0OOO0000O0 :#line:131
            O0000OOO00OOOOOOO =O00O00O0OOO0000O0 .pop ("base_path")#line:132
        for O000O0O0000O0000O in O00O00O0OOO0000O0 :#line:133
            for OOO0OOOO0O0OO0OOO in O00O00O0OOO0000O0 [O000O0O0000O0000O ].split ("\n"):#line:134
                if len (OOO0OOOO0O0OO0OOO )==0 :#line:135
                    continue #line:136
                O0000O0OOO0OOO000 =OOO0OOOO0O0OO0OOO #line:137
                if O0000OOO00OOOOOOO is not None :#line:138
                    O0000O0OOO0OOO000 =os .path .join (O0000OOO00OOOOOOO ,O0000O0OOO0OOO000 )#line:139
                print ("Adding extra search path",O000O0O0000O0000O ,O0000O0OOO0OOO000 )#line:140
                folder_paths .add_model_folder_path (O000O0O0000O0000O ,O0000O0OOO0OOO000 )#line:141
if __name__ =="__main__":#line:144
    if args .temp_directory :#line:145
        temp_dir =os .path .join (os .path .abspath (args .temp_directory ),"temp")#line:146
        print (f"Setting temp directory to: {temp_dir}")#line:147
        folder_paths .set_temp_directory (temp_dir )#line:148
    cleanup_temp ()#line:149
    loop =asyncio .new_event_loop ()#line:151
    asyncio .set_event_loop (loop )#line:152
    server =server .PromptServer (loop )#line:153
    q =execution .PromptQueue (server )#line:154
    extra_model_paths_config_path =os .path .join (os .path .dirname (os .path .realpath (__file__ )),"extra_model_paths.yaml")#line:156
    if os .path .isfile (extra_model_paths_config_path ):#line:157
        load_extra_path_config (extra_model_paths_config_path )#line:158
    if args .extra_model_paths_config :#line:160
        for config_path in itertools .chain (*args .extra_model_paths_config ):#line:161
            load_extra_path_config (config_path )#line:162
    init_custom_nodes ()#line:164
    cuda_malloc_warning ()#line:166
    server .add_routes ()#line:168
    hijack_progress (server )#line:169
    threading .Thread (target =prompt_worker ,daemon =True ,args =(q ,server ,)).start ()#line:171
    if args .output_directory :#line:173
        output_dir =os .path .abspath (args .output_directory )#line:174
        print (f"Setting output directory to: {output_dir}")#line:175
        folder_paths .set_output_directory (output_dir )#line:176
    if args .quick_test_for_ci :#line:178
        exit (0 )#line:179
    call_on_start =None #line:181
    if args .auto_launch :#line:182
        def startup_server (OO00OOOO0OO00OOO0 ,O0OO00000O0OOO00O ):#line:183
            import webbrowser #line:184
            if os .name =='nt'and OO00OOOO0OO00OOO0 =='0.0.0.0':#line:185
                OO00OOOO0OO00OOO0 ='127.0.0.1'#line:186
            webbrowser .open (f"http://{OO00OOOO0OO00OOO0}:{O0OO00000O0OOO00O}")#line:187
        call_on_start =startup_server #line:188
    try :#line:190
        loop .run_until_complete (run (server ,address =args .listen ,port =args .port ,verbose =not args .dont_print_server ,call_on_start =call_on_start ))#line:191
    except KeyboardInterrupt :#line:192
        print ("\nStopped server")#line:193
    cleanup_temp ()#line:195
