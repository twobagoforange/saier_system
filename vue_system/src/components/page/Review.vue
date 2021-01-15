<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class='el-icon-lx-question'></i> 审核题目
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="handle-box">
                <el-button
                        type="primary"
                        icon="el-icon-delete"
                        class="handle-del mr10"
                        @click="passAllSelection"
                >批量通过
                </el-button>
            </div>
            <el-table
                    :data="tableData"
                    border
                    class="table"
                    ref="multipleTable"
                    stripe="true"
                    header-cell-class-name="table-header"
                    @selection-change="handleSelectionChange"
            >
                <el-table-column type="selection" width="55" align="center"></el-table-column>
                <el-table-column type="expand">
                    <template slot-scope="props">
                        <el-form label-position="left" inline class="demo-table-expand">
                            <el-form-item label="题目">
                                <span>{{ props.row.ques_body }}</span>
                            </el-form-item>
                            <el-form-item label="选项A">
                                <span>{{ props.row.item_a }}</span>
                            </el-form-item>
                            <el-form-item label="选项B">
                                <span>{{ props.row.item_b }}</span>
                            </el-form-item>
                            <el-form-item label="选项C">
                                <span>{{ props.row.item_c }}</span>
                            </el-form-item>
                            <el-form-item label="选项D">
                                <span>{{ props.row.item_d }}</span>
                            </el-form-item>
                            <el-form-item label="答案">
                                <span>{{ props.row.corr_ans }}</span>
                            </el-form-item>
                            <el-form-item label="解析">
                                <span>{{ props.row.analysis }}</span>
                            </el-form-item>
                            <el-form-item label="出题人">
                                <span>{{ props.row.author }}</span>
                            </el-form-item>
                        </el-form>
                    </template>
                </el-table-column>
                <el-table-column prop="seq" label="序号" width="55" align="center"></el-table-column>
                <el-table-column prop="ques_body" label="题目" width="700" align="center"></el-table-column>
                <el-table-column prop="status" label="状态" align="center">
                </el-table-column>

                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                                type="text"
                                icon="el-icon-circle-check"
                                @click="handleEdit(scope.$index, scope.row)"
                        >通过
                        </el-button>
                        <el-button
                                type="text"
                                icon="el-icon-circle-close"
                                class="red"
                                @click="handleDelete(scope.$index, scope.row)"
                        >未通过
                        </el-button>
                    </template>
                </el-table-column>

            </el-table>
            <div class="pagination">
                <el-pagination
                        background
                        layout="total, prev, pager, next"
                        :current-page="pageIndex"
                        :page-size="pageSize"
                        :total="pageTotal"
                        @current-change="handlePageChange"
                ></el-pagination>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'review',
        data() {
            return {
                tableData: [],
                multipleSelection: [],
                passList: [],
                editVisible: false,
                pageTotal: 0,
                form: {},
                idx: -1,
                seq: -1,
                pageIndex: 1,
                pageSize: 10
            };
        },
        created() {
            this.getData();
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                axios({
                    method: 'get',
                    url: 'http://127.0.0.1:8000/api/show_pending_ques',
                    xsrfCookieName: '',
                    withCredentials: true
                }).then((res) => {
                    if (res.data.error_num == 0) {
                        this.tableData = res.data.list;
                        this.pageTotal = res.data.pageTotal || 50;
                    }
                    console.log(res);
                });
            },
            // 删除操作
            handleDelete(index, row) {
                this.idx = index;
                this.form = row;
                this.editVisible = true;
                axios({
                    method: 'get',
                    url: 'http://127.0.0.1:8000/api/set_ques_status',
                    params: {
                        'id': this.tableData[this.idx]['id'],
                        'status': '认证未通过'
                    },
                    xsrfCookieName: '',
                    withCredentials: true
                }).then((res) => {
                    if (res.data.error_num == 0) {
                        this.$message.success('操作成功！');
                        // this.$set(this.tableData, this.idx, this.form);
                        this.tableData.splice(this.idx, 1);
                    }
                    console.log(res);
                });
                // this.$router.push('/review');
            },
            // 多选操作
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            passAllSelection() {
                const length = this.multipleSelection.length;
                let str = '';
                let i = 0;
                for (i ; i < length - 1; i++) {
                    str = str + this.multipleSelection[i].id + ',';
                }
                str = str + this.multipleSelection[i].id;
                // 二次确认通过;
                this.$confirm('确定要批量通过审核吗？', '提示', {
                    type: 'warning'
                })
                    .then(() => {
                        axios({
                            method: 'get',
                            url: 'http://127.0.0.1:8000/api/set_ques_status_by_list',
                            params: {
                                'passList': str,
                                'status': '认证通过'
                            },
                            xsrfCookieName: '',
                            withCredentials: true
                        }).then((res) => {
                            if (res.data.error_num == 0) {
                                this.form = res.data.list;
                                this.$message.success('通过成功');
                                // this.tableData.splice(this.idx, )
                                this.getData();
                            }
                            console.log(res);
                        });
                    })
                    .catch(() => {
                    });
                this.multipleSelection = [];
            },
            // 编辑操作
            handleEdit(index, row) {
                this.idx = index;
                this.form = row;
                this.editVisible = true;
                axios({
                    method: 'get',
                    url: 'http://127.0.0.1:8000/api/set_ques_status',
                    // headers: {
                    //     'Content-Type': 'multipart/form-data'
                    // },
                    params: {
                        'id': this.tableData[this.idx]['id'],
                        'status': '认证通过'
                    },
                    xsrfCookieName: '',
                    withCredentials: true
                }).then((res) => {
                    if (res.data.error_num == 0) {
                        this.$message.success('操作成功！');
                        this.tableData.splice(this.idx, 1);
                    }
                    console.log(res);
                });
                // this.$router.push('/review');
            },
            // 保存编辑
            saveEdit() {
                this.editVisible = false;
                this.$message.success(`修改第 ${this.idx + 1} 行成功`);
                this.$set(this.tableData, this.idx, this.form);
            },
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            }
        }
    };
</script>

<style>
    .demo-table-expand {
        font-size: 0;
    }

    .demo-table-expand label {
        width: 90px;
        color: #99a9bf;
    }

    .demo-table-expand .el-form-item {
        margin-right: 0;
        margin-bottom: 0;
        width: 100%;
    }
</style>

<style scoped>
    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
    }

    .handle-input {
        width: 300px;
        display: inline-block;
    }

    .table {
        width: 100%;
        font-size: 14px;
    }

    .red {
        color: #ff0000;
    }

    .mr10 {
        margin-right: 10px;
    }

    .table-td-thumb {
        display: block;
        margin: auto;
        width: 40px;
        height: 40px;
    }
</style>
