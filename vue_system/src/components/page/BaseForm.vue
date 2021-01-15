<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class='el-icon-lx-text'></i> 我要出题
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <el-form ref="form" :model="form" label-width="100px" style="width:800px;">
                    <el-form-item label="关联知识点">
                        <el-select v-model="form.key" placeholder="请选择" style="width:800px;">
                            <el-option key="chapter5" label="第五章 指令系统" value="chapter5"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="题型">
                        <el-select v-model="form.type" placeholder="请选择" style="width:800px;">
                            <el-option key="chapter5" label="单选" value="chapter5"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="题目">
                        <el-input type="textarea" rows="5" v-model="form.ques_body" style="width:800px;"
                                  placeholder="请输入题目"></el-input>
                    </el-form-item>
                    <el-form-item label="题目选项">
                        <el-radio-group v-model="form.corr_ans" @change="agreeChange">
                            <el-col :span="23">
                                <el-tag effect="plain" size="medium">A.</el-tag>
                                <el-input v-model="form.item_a" placeholder="请输入选项"
                                          style="margin-bottom:5px;width:600px;"></el-input>
                            </el-col>
                            <el-col :span="1">
                                <el-radio label="1" border="5px">设为答案</el-radio>
                            </el-col>
                            <el-col :span="23">
                                <el-tag effect="plain" size="medium">B.</el-tag>
                                <el-input v-model="form.item_b" placeholder="请输入选项"
                                          style="margin-bottom:5px;width:600px;"></el-input>
                            </el-col>
                            <el-col :span="1">
                                <el-radio label="2" border="5px">设为答案</el-radio>
                            </el-col>
                            <el-col :span="23">
                                <el-tag effect="plain" size="medium">C.</el-tag>
                                <el-input v-model="form.item_c" placeholder="请输入选项"
                                          style="margin-bottom:5px;width:600px;"></el-input>
                            </el-col>
                            <el-col :span="1">
                                <el-radio label="3" border="5px">设为答案</el-radio>
                            </el-col>
                            <el-col :span="23">
                                <el-tag effect="plain" size="medium">D.</el-tag>
                                <el-input v-model="form.item_d" placeholder="请输入选项"
                                          style="margin-bottom:5px;width:600px;"></el-input>
                            </el-col>
                            <el-col :span="1">
                                <el-radio label="4" border="5px">设为答案</el-radio>
                            </el-col>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="题目解析">
                        <el-input type="textarea" rows="5" v-model="form.analysis" placeholder="请输入题目解析"
                                  style="width:800px;"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">提交</el-button>
                        <el-button @click="onCancel">取消</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>

    import axios from 'axios';

    export default {
        name: 'baseform',
        data() {
            return {
                form: {
                    key: '',
                    type: '',
                    ques_body: '',
                    corr_ans: '1',
                    item_a: '',
                    item_b: '',
                    item_c: '',
                    item_d: '',
                    analysis: ''
                }
            };
        },
        created() {
            if (this.$route.query.quesId != null) {
                axios({
                    method: 'get',
                    url: 'http://127.0.0.1:8000/api/get_ques_by_id',
                    params: { 'id': this.$route.query.quesId },
                    xsrfCookieName: '',
                    withCredentials: true
                }).then((res) => {
                    if (res.data.error_num == 0) {
                        this.form = res.data.list;

                    }
                    console.log(res);
                });
            }
        },
        methods: {
            onSubmit() {
                let formData = new FormData();
                formData.append('username', localStorage.getItem('ms_username'));
                if (this.$route.query.quesId != null){
                    formData.append('ques_id', this.$route.query.quesId);
                }
                else {
                    formData.append('ques_id', -1);
                }
                for (var key in this.form) {
                    formData.append(key, this.form[key]);
                }

                axios({
                    method: 'post',
                    url: 'http://127.0.0.1:8000/api/add_ques',
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    xsrfCookieName: '',
                    withCredentials: true,
                    data: formData
                }).then((res) => {
                    if (res.data.error_num == 0) {
                        this.$message.success('提交成功！');
                        this.$router.push('/table');
                        axios({
                            method: 'get',
                            url: 'http://127.0.0.1:8000/api/get_ques_judge',
                            headers: {
                                'Content-Type': 'multipart/form-data'
                            },
                            params: { 'ques_id': res.data.ques_id },
                            xsrfCookieName: '',
                            withCredentials: true,
                            data: formData
                        }).then((ans) => {
                            if (ans.data.error_num == 0) {
                            }
                            console.log(ans);
                        });
                    }
                    console.log(res);
                });
            },
            onCancel() {
                this.$router.push('/table');
            }
        }
    };
</script>