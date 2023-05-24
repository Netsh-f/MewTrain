<template>
    <div class="fillcontain">
        <meta  http-equiv="Cache-Control" content="no-cache,no-store,must-revlidate">
        <meta  http-equiv="Expires" content="O">
        <meta http-equiv="Pragma" content="no-cache">

        <el-form :model="searchForm"  ref="searchForm">
            <el-row :gutter="20" style="margin-left: 180px;margin-top: 10px;width: 1000px">
                <el-col :span="6"><div class="grid-content bg-purple">
                    <el-autocomplete
                        class="inline-input"
                        v-model="searchForm.start_station"
                        :fetch-suggestions="querySearch"
                        placeholder="请输入始发站"
                        :trigger-on-focus="true"
                        @select="handleSelect"
                    ></el-autocomplete>
                </div></el-col>
                <el-col :span="6"><div class="grid-content bg-purple" style="margin-left: 20px">
                    <el-autocomplete
                        class="inline-input"
                        v-model="searchForm.end_station"
                        :fetch-suggestions="querySearch"
                        placeholder="请输入终点站"
                        :trigger-on-focus="true"
                        @select="handleSelect"
                    ></el-autocomplete>
                </div></el-col>
                <el-col :span="6"><div class="grid-content bg-purple" style="margin-left: 20px">
                    <div class="block">
                        <el-date-picker
                            v-model="searchForm.datetime"
                            type="date"
                            placeholder="选择日期">
                        </el-date-picker>
                    </div>
                </div></el-col>
                <el-col :span="6"><div class="grid-content bg-purple">
                    <!-- 点击时调用submitForm函数并传递 searchForm参数-->
                    <el-button type="primary" round  @click="submitForm('searchForm')">搜索</el-button>
                </div></el-col>
                <el-switch
                    style="margin-top: 30px;margin-left: 20px"
                    v-model="value1"
                    @click.self="handelUpdate()"
                    inactive-text="按开车时间排序"
                    active-text="按运行时间排序">
                </el-switch>
            </el-row>
        </el-form>
        <div class="table_container">
            <el-table
                :data="tableData"
                style="width: 100%"
                row-key="train_number">

                <el-table-column
                    label="车次"
                    prop="train_number">
                </el-table-column>
                <el-table-column
                    label="出发站"
                    prop="start_station">
                </el-table-column>
                <el-table-column
                    label="到达站"
                    prop="end_station">
                </el-table-column>
                <el-table-column
                    label="出发时间"
                    prop="start_time">
                </el-table-column>
                <el-table-column
                    label="到达时间"
                    prop="arrive_time">
                </el-table-column>
                <el-table-column
                    label="特等座/软卧"
                    prop="high_seat_price">
                </el-table-column>
                <el-table-column
                    label="一等座/硬卧"
                    prop="medium_seat_price">
                </el-table-column>
                <el-table-column
                    label="二等座/硬座"
                    prop="low_seat_price">
                </el-table-column>
                <el-table-column label="操作" width="200">
                    <template v-slot:default="scope">
                        <!-- 跳转至查询 -->
                        <el-button
                            size="mini"
                            @click="handleSearch(scope.$index,searchForm.datetime,scope.row.train_no,scope.row.start_no,scope.row.end_no,scope.row.train_number)">查看余票</el-button>
                        <!-- 跳转至购买 -->
                        <el-button
                            size="mini"
                            type="Success"
                            @click="handleBuy(scope.$index,searchForm.datetime,scope.row.train_no,scope.row.start_no,scope.row.end_no,
                            scope.row.train_number,scope.row.high_seat_price,scope.row.medium_seat_price,scope.row.low_seat_price)">预定</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <!-- Table -->

            <el-dialog title="余座数" v-model="dialogTableVisible_GD" style="width: 1500px">
                <el-table :data="high_seat_GD">
                  <el-table-column property="carriage_number" label="车厢号" width="150"></el-table-column>
                  <el-table-column property="seat_type" label="座位类型" width="200"></el-table-column>
                  <el-table-column property="A_num" label="A座"></el-table-column>
                  <el-table-column property="B_num" label="B座"></el-table-column>
                  <el-table-column property="C_num" label="C座"></el-table-column>
                </el-table>
                <el-table :data="medium_seat_GD">
                  <el-table-column property="carriage_number" label="车厢号" width="150"></el-table-column>
                  <el-table-column property="seat_type" label="座位类型" width="200"></el-table-column>
                  <el-table-column property="A_num" label="A座"></el-table-column>
                  <el-table-column property="B_num" label="B座"></el-table-column>
                  <el-table-column property="C_num" label="C座"></el-table-column>
                  <el-table-column property="D_num" label="D座"></el-table-column>
                </el-table>
                <el-table :data="low_seat_GD">
                  <el-table-column property="carriage_number" label="车厢号" width="150"></el-table-column>
                  <el-table-column property="seat_type" label="座位类型" width="200"></el-table-column>
                  <el-table-column property="A_num" label="A座"></el-table-column>
                  <el-table-column property="B_num" label="B座"></el-table-column>
                  <el-table-column property="C_num" label="C座"></el-table-column>
                  <el-table-column property="D_num" label="D座"></el-table-column>
                  <el-table-column property="E_num" label="E座"></el-table-column>
                </el-table>
              </el-dialog>


            <el-dialog title="余座数" v-model="dialogTableVisible" style="width: 1500px">
                <el-table :data="high_seat">

                    <el-table-column property="carriage_number" label="车厢号" width="150"></el-table-column>
                    <el-table-column property="seat_type" label="座位类型" width="200"></el-table-column>
                    <el-table-column property="upper_num" label="上铺"></el-table-column>
                    <el-table-column property="lower_num" label="下铺"></el-table-column>
                </el-table>
                <el-table :data="medium_seat">

                    <el-table-column property="carriage_number" label="车厢号" width="150"></el-table-column>
                    <el-table-column property="seat_type" label="座位类型" width="200"></el-table-column>
                    <el-table-column property="upper_num" label="上铺"></el-table-column>
                    <el-table-column property="middle_num" label="中铺"></el-table-column>
                    <el-table-column property="lower_num" label="下铺"></el-table-column>
                </el-table>
                <el-table :data="low_seat">

                    <el-table-column property="carriage_number" label="车厢号" width="150"></el-table-column>
                    <el-table-column property="seat_type" label="座位类型" width="200"></el-table-column>
                    <el-table-column property="A_num" label="A座"></el-table-column>
                    <el-table-column property="B_num" label="B座"></el-table-column>
                    <el-table-column property="C_num" label="C座"></el-table-column>
                    <el-table-column property="D_num" label="D座"></el-table-column>
                    <el-table-column property="E_num" label="E座"></el-table-column>
                    <el-table-column property="F_num" label="F座"></el-table-column>
                </el-table>
            </el-dialog>
        </div>
    </div>
</template>
<script>
    import {queryTrainTicket,getAllStationName} from '../api/getData'
    export default {
        data(){
            return {
                value1: false,
                tableData: [
                ],
                selectTable: {},
                searchForm:
                    {
                        start_station: '',
                        end_station:"",
                        datetime:""

                    },
                high_seat:[
                    {
                        carriage_number:"1",
                        seat_type:"2",
                        upper_num:"3",
                        lower_num:"4"
                    }
                ],
                medium_seat:[
                    {
                        carriage_number:"1",
                        seat_type:"2",
                        upper_num:"3",
                        middle_num:"5",
                        lower_num:"4"
                    }
                ],
                low_seat:[
                    {
                        carriage_number:"1",
                        seat_type:"2",
                        A_num:"3",
                        B_num:"5",
                        C_num:"4",
                        D_num:"4",
                        E_num:"4",
                        F_num:"4"
                    }
                ],
                high_seat_GD:[
                    {
                        carriage_number:"1",
                        seat_type:"2",
                        A_num:"3",
                        B_num:"5",
                        C_num:"4"
                    }
                ],
                medium_seat_GD:[
                    {
                        carriage_number:"1",
                        seat_type:"2",
                        A_num:"3",
                        B_num:"5",
                        C_num:"4",
                        D_num:"4"
                    }
                ],
                low_seat_GD:[
                    {
                        carriage_number:"1",
                        seat_type:"2",
                        A_num:"3",
                        B_num:"5",
                        C_num:"4",
                        D_num:"4",
                        E_num:"4"
                    }
                ],
                dialogTableVisible: false,
                dialogTableVisible_GD: false,
                form: {
                    name: '',
                    region: '',
                    date1: '',
                    date2: '',
                    delivery: false,
                    type: [],
                    resource: '',
                    desc: ''
                },
                formLabelWidth: '120px',
                stationData:[],
            }
        },
        methods: {
            async created(){
            const res = await getAllStationName()
            this.stationData = res.dataLists;
        },
            // queryString是用户在输入框中输入的文本字符串，用于进行搜索。cb是一个回调函数，用于在搜索完成时将搜索结果传递给自动完成组件。
            //从"stationData"属性中获取所有的车站数据列表，存储在"houseNumberList"变量中。
            //根据用户输入的queryString字符串，通过调用"createFilter"方法创建一个过滤函数，用于过滤出符合条件的车站数据列表。
            async querySearch(queryString, cb) {
                var houseNumberList = this.stationData;
                let results = queryString ? houseNumberList.filter(this.createFilter(queryString)) : houseNumberList;
                //延时
                clearTimeout(this.timeout);
                this.timeout = setTimeout(() => {
                     cb(results);
                }, 1000 * Math.random());

            },
            //先调用this.$refs[formName].validate方法验证表单数据的有效性,有效再进行操作
            async submitForm(formName) {
                this.$refs[formName].validate(async (valid) => {
                    if (valid) {
                        let date;
                        //将表单中的数据转换为date格式
                        date= new Date(this.searchForm.datetime);

                        let datetime2 = date.getFullYear()+'-'+this.checkTime(date.getMonth()+1)+'-'+this.checkTime(date.getDate());
                        this.tableData = [];
                        //调用异步请求方法queryTrainTicket，根据表单中填写的出发地、目的地和日期时间等信息，从后端API获取符合条件的列车信息。
                        const res = await queryTrainTicket({train_start_station:this.searchForm.start_station , train_end_station:this.searchForm.end_station ,datetime :datetime2})
                            if(res.status == 1)
                            {
                                this.$message({
                                    type: 'success',
                                    message: '查询成功'
                                });
                                this.tableData = [];
                                for(let i = 0 ; i < res.trainTicketPriceInfoList.length ; i++ )
                                {
                                    const tableData = {};
                                    tableData.train_no = res.trainTicketPriceInfoList[i].train_no;
                                    tableData.train_number = res.trainTicketPriceInfoList[i].train_number;
                                    tableData.start_station =res.trainTicketPriceInfoList[i].start_station;
                                    tableData.end_station = res.trainTicketPriceInfoList[i].end_station;
                                    tableData.start_time =res.trainTicketPriceInfoList[i].start_time;
                                    tableData.arrive_time = res.trainTicketPriceInfoList[i].arrive_time;
                                    tableData.high_seat_price = res.trainTicketPriceInfoList[i].high_seat_price;
                                    tableData.medium_seat_price = res.trainTicketPriceInfoList[i].medium_seat_price ;
                                    tableData.low_seat_price = res.trainTicketPriceInfoList[i].low_seat_price;
                                    tableData.end_no = res.trainTicketPriceInfoList[i].end_no;
                                    tableData.start_no =res.trainTicketPriceInfoList[i].start_no;

                                    this.tableData.push(tableData);
                                }
                                console.log(this.tableData)
                                this.TrainRank();
                            }
                            else if(res.status == 404)
                            {
                                this.$message({
                                    type: 'error',
                                    message: '没有符合条件的列车'
                                });
                            }else if(res.status == 406)
                            {
                                this.$message({
                                    type: 'error',
                                    message: '没有符合条件的列车'
                                });
                            }
                            else {
                                this.$message({
                                    type: 'error',
                                    message: '查询失败'
                                });
                            }
                    }

                });
            },

        },
        //对查询的信息进行排序
        TrainRank()
            {
                if(this.value1 === false)
                {
                    for(let i = 0 ; i < this.tableData.length ; i++)
                    {
                        for(let j = 0 ; j <this.tableData.length - i -1 ; j++ )
                        {
                            if(this.transferTime(this.tableData[j].start_time) >this.transferTime(this.tableData[j+1].start_time))
                            {
                                let temp = this.tableData[j];
                                this.tableData[j] = this.tableData[j+1];
                                this.tableData[j+1] = temp;
                            }
                        }
                    }
                }
                else
                {
                    for(let i = 0 ; i < this.tableData.length ; i++)
                    {
                        for(let j = 0 ; j <this.tableData.length - i -1 ; j++ )
                        {
                            if(this.transferTime(this.tableData[j].running_time) >this.transferTime(this.tableData[j+1].running_time))
                            {
                                let temp = this.tableData[j];
                                this.tableData[j] = this.tableData[j+1];
                                this.tableData[j+1] = temp;
                            }
                        }
                    }
                }
            },
            handleBuy(index,datetime,train_no,start_no,end_no,train_number,high_seat_price,medium_seat_price,low_seat_price)
            {
                let date;
                date= new Date(datetime);
                console.log("date"+date);
                console.log("train_no"+typeof train_number);
                let datetime2 = date.getFullYear()+'-'+this.checkTime(date.getMonth()+1)+'-'+this.checkTime(date.getDate());
                this.$router.push({
                    path: '/TicketOrder',
                    query: {
                        datetime: datetime2,
                        train_no: train_no,
                        start_no:start_no,
                        end_no:end_no,
                        train_number:train_number,
                        high_seat_price:high_seat_price,
                        medium_seat_price:medium_seat_price,
                        low_seat_price:low_seat_price
                    }
                    /*query: {
                        key: 'key',
                        msgKey: this.msg
                    }*/
                })
            },
            handelUpdate()
            {
                this.TrainRank();

            },
            createFilter(queryString) {
                return (houseNumber) => {
                    return (houseNumber.value.toLowerCase().indexOf(queryString.toLowerCase()) !== -1);
                };
            },
            checkTime(i){
                if(i<10){
                    i = '0'+i
                }

                return i
            },
    }
</script>

<style lang="less">
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
        width: 50%;
    }
    .table_container{
        padding: 20px;
    }
    .Pagination{
        display: flex;
        justify-content: flex-start;
        margin-top: 8px;
    }
    .avatar-uploader .el-upload {
        border: 1px dashed #d9d9d9;
        border-radius: 6px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    .avatar-uploader .el-upload:hover {
        border-color: #20a0ff;
    }
    .avatar-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        width: 120px;
        height: 120px;
        line-height: 120px;
        text-align: center;
    }
    .avatar {
        width: 120px;
        height: 120px;
        display: block;
    }
</style>