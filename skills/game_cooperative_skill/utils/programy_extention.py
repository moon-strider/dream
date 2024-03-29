# Copyright 2017 Neural Networks and Deep Learning lab, ***REMOVED***
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from programy.clients.embed.basic import EmbeddedDataFileBot


class MindfulDataFileBot(EmbeddedDataFileBot):
    def ask_question(self, userid, question):
        client_context = self.create_client_context(userid)
        return self.renderer.render(client_context, self.process_question(client_context, question))
