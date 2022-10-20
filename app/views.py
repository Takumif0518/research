from django.shortcuts import render
from .models import QUEST , IO
from django.http import Http404
from django.views import generic
import datetime , os , subprocess
from .forms import EditorForm
from django.urls import reverse_lazy
from django.conf import settings

file_dir = os.path.join(settings.BASE_DIR, 'history') #パスの統合(プログラムを格納するディレクトリへの絶対パス)
docker_cmd = 'docker run -i --rm --name my-running-script -v {}:/usr/src/myapp -w /usr/src/myapp python:3.7 python {}' #{}は置換フィールド29行目format()で置換


def choice(request):
    question_list = QUEST.objects.order_by('question_id')
    context = {'question_list': question_list}
    return render(request, 'choice.html', context)

def detail(request,question_id):
    try:
        question = QUEST.objects.get(pk=question_id)
    except QUEST.DoesNotExist:
        raise Http404("QUEST does not exist")
    return render(request, 'detail.html', {'question': question})

class Home(generic.FormView): #FormView : POST
    template_name = 'home.html'
    form_class = EditorForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """送信ボタンでよびだされる."""
        code = form.cleaned_data['code']
        output = start_docker(code)
        context = self.get_context_data(form=form, output=output)
        return self.render_to_response(context) #ページの更新

def start_docker(code):
    """dockerコンテナ内でPythonコードを実行する."""
    # historyディレクトリ内に、2019-07-29T22:58:24.1111.py のようなファイルを作り、中身は入力したコード
    file_name = '{}.py'.format(datetime.datetime.now().isoformat()) #.isoformat() == 日付を ISO 8601 書式の YYYY-MM-DDの文字列で返す
    file_path = os.path.join(file_dir, file_name) #保存するプログラムファイルのパス
    with open(file_path, 'w', encoding='utf-8') as file: #→file=open(...)
        file.write(code) #引数として受け取ったコードを書き込む

    '''with A as B:
        処理X
        
        開始・終了の処理が必要なAをB=Aで開始して処理Xをした後に終了する'''
    for _ in range(10):
        cmd = docker_cmd.format(file_dir, file_name) #format関数で{}に適切な値を入れコマンドを完成させる
        ret = subprocess.run( #subprocess 他のアプリを呼び出す　標準ライブラリの1つ
            cmd, timeout=15, shell=True, #timeout[s]:タイムアウト時間[秒]　　shell:＝trueで標準shellを使用
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT  #stdout:標準出力 stderr:標準エラー
        )
    return ret.stdout.decode()

