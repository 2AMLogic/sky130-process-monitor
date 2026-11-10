module readout (busy,
    clk_ref,
    done,
    overflow,
    rst_n,
    we,
    addr,
    osc,
    rdata,
    wdata);
 output busy;
 input clk_ref;
 output done;
 output overflow;
 input rst_n;
 input we;
 input [3:0] addr;
 input [4:0] osc;
 output [23:0] rdata;
 input [23:0] wdata;

 wire _0000_;
 wire _0001_;
 wire _0002_;
 wire _0003_;
 wire _0004_;
 wire _0005_;
 wire _0006_;
 wire _0007_;
 wire _0008_;
 wire _0009_;
 wire _0010_;
 wire _0011_;
 wire _0012_;
 wire _0013_;
 wire _0014_;
 wire _0015_;
 wire _0016_;
 wire _0017_;
 wire _0018_;
 wire _0019_;
 wire _0020_;
 wire _0021_;
 wire _0022_;
 wire _0023_;
 wire _0024_;
 wire _0025_;
 wire _0026_;
 wire _0027_;
 wire _0028_;
 wire _0029_;
 wire _0030_;
 wire _0031_;
 wire _0032_;
 wire _0033_;
 wire _0034_;
 wire _0035_;
 wire _0036_;
 wire _0037_;
 wire _0038_;
 wire _0039_;
 wire _0040_;
 wire _0041_;
 wire _0042_;
 wire _0043_;
 wire _0044_;
 wire _0045_;
 wire _0046_;
 wire _0047_;
 wire _0048_;
 wire _0049_;
 wire _0050_;
 wire _0051_;
 wire _0052_;
 wire _0053_;
 wire _0054_;
 wire _0055_;
 wire _0056_;
 wire _0057_;
 wire _0058_;
 wire _0059_;
 wire _0060_;
 wire _0061_;
 wire _0062_;
 wire _0063_;
 wire _0064_;
 wire _0065_;
 wire _0066_;
 wire _0067_;
 wire _0068_;
 wire _0069_;
 wire _0070_;
 wire _0071_;
 wire _0072_;
 wire _0073_;
 wire _0074_;
 wire _0075_;
 wire _0076_;
 wire _0077_;
 wire _0078_;
 wire _0079_;
 wire _0080_;
 wire _0081_;
 wire _0082_;
 wire _0083_;
 wire _0084_;
 wire _0085_;
 wire _0086_;
 wire _0087_;
 wire _0088_;
 wire _0089_;
 wire _0090_;
 wire _0091_;
 wire _0092_;
 wire _0093_;
 wire _0094_;
 wire _0095_;
 wire _0096_;
 wire _0097_;
 wire _0098_;
 wire _0099_;
 wire _0100_;
 wire _0101_;
 wire _0102_;
 wire _0103_;
 wire _0104_;
 wire _0105_;
 wire _0106_;
 wire _0107_;
 wire _0108_;
 wire _0109_;
 wire _0110_;
 wire _0111_;
 wire _0112_;
 wire _0113_;
 wire _0114_;
 wire _0115_;
 wire _0116_;
 wire _0117_;
 wire _0118_;
 wire _0119_;
 wire _0120_;
 wire _0121_;
 wire _0122_;
 wire _0123_;
 wire _0124_;
 wire _0125_;
 wire _0126_;
 wire _0127_;
 wire _0128_;
 wire _0129_;
 wire _0130_;
 wire _0131_;
 wire _0132_;
 wire _0133_;
 wire _0134_;
 wire _0135_;
 wire _0136_;
 wire _0137_;
 wire _0138_;
 wire _0139_;
 wire _0140_;
 wire _0141_;
 wire _0142_;
 wire _0143_;
 wire _0144_;
 wire _0145_;
 wire _0146_;
 wire _0147_;
 wire _0148_;
 wire _0149_;
 wire _0150_;
 wire _0151_;
 wire _0152_;
 wire _0153_;
 wire _0154_;
 wire _0155_;
 wire _0156_;
 wire _0157_;
 wire _0158_;
 wire _0159_;
 wire _0160_;
 wire _0161_;
 wire _0162_;
 wire _0163_;
 wire _0164_;
 wire _0165_;
 wire _0166_;
 wire _0167_;
 wire _0168_;
 wire _0169_;
 wire _0170_;
 wire _0171_;
 wire _0172_;
 wire _0173_;
 wire _0174_;
 wire _0175_;
 wire _0176_;
 wire _0177_;
 wire _0178_;
 wire _0179_;
 wire _0180_;
 wire _0181_;
 wire _0182_;
 wire _0183_;
 wire _0184_;
 wire _0185_;
 wire _0186_;
 wire _0187_;
 wire _0188_;
 wire _0189_;
 wire _0190_;
 wire _0191_;
 wire _0192_;
 wire _0193_;
 wire _0194_;
 wire _0195_;
 wire _0196_;
 wire _0197_;
 wire _0198_;
 wire _0199_;
 wire _0200_;
 wire _0201_;
 wire _0202_;
 wire _0203_;
 wire _0204_;
 wire _0205_;
 wire _0206_;
 wire _0207_;
 wire _0208_;
 wire _0209_;
 wire _0210_;
 wire _0211_;
 wire _0212_;
 wire _0213_;
 wire _0214_;
 wire _0215_;
 wire _0216_;
 wire _0217_;
 wire _0218_;
 wire _0219_;
 wire _0220_;
 wire _0221_;
 wire _0222_;
 wire _0223_;
 wire _0224_;
 wire _0225_;
 wire _0226_;
 wire _0227_;
 wire _0228_;
 wire _0229_;
 wire _0230_;
 wire _0231_;
 wire _0232_;
 wire _0233_;
 wire _0234_;
 wire _0235_;
 wire _0236_;
 wire _0237_;
 wire _0238_;
 wire _0239_;
 wire _0240_;
 wire _0241_;
 wire _0242_;
 wire _0243_;
 wire _0244_;
 wire _0245_;
 wire _0246_;
 wire _0247_;
 wire _0248_;
 wire _0249_;
 wire _0250_;
 wire _0251_;
 wire _0252_;
 wire _0253_;
 wire _0254_;
 wire _0255_;
 wire _0256_;
 wire _0257_;
 wire _0258_;
 wire _0259_;
 wire _0260_;
 wire _0261_;
 wire _0262_;
 wire _0263_;
 wire _0264_;
 wire _0265_;
 wire _0266_;
 wire _0267_;
 wire _0268_;
 wire _0269_;
 wire _0270_;
 wire _0271_;
 wire _0272_;
 wire _0273_;
 wire _0274_;
 wire _0275_;
 wire _0276_;
 wire _0277_;
 wire _0278_;
 wire _0279_;
 wire _0280_;
 wire _0281_;
 wire _0282_;
 wire _0283_;
 wire _0284_;
 wire _0285_;
 wire _0286_;
 wire _0287_;
 wire _0288_;
 wire _0289_;
 wire _0290_;
 wire _0291_;
 wire clknet_leaf_4_clk_ref;
 wire _0293_;
 wire _0294_;
 wire _0295_;
 wire _0296_;
 wire _0297_;
 wire _0298_;
 wire clknet_leaf_5_clk_ref;
 wire _0300_;
 wire _0301_;
 wire _0302_;
 wire _0303_;
 wire _0304_;
 wire _0305_;
 wire _0306_;
 wire _0307_;
 wire _0308_;
 wire _0309_;
 wire _0310_;
 wire _0311_;
 wire _0312_;
 wire _0313_;
 wire _0314_;
 wire _0315_;
 wire clknet_leaf_29_clk_ref;
 wire _0317_;
 wire _0318_;
 wire clknet_leaf_28_clk_ref;
 wire _0320_;
 wire _0321_;
 wire _0322_;
 wire _0323_;
 wire _0324_;
 wire _0325_;
 wire _0326_;
 wire _0327_;
 wire _0328_;
 wire net18;
 wire _0330_;
 wire _0331_;
 wire _0332_;
 wire _0333_;
 wire _0334_;
 wire _0335_;
 wire _0336_;
 wire _0337_;
 wire _0338_;
 wire _0339_;
 wire clknet_2_0__leaf_clk_ref;
 wire clknet_0_clk_ref;
 wire _0342_;
 wire _0343_;
 wire _0344_;
 wire clknet_leaf_30_clk_ref;
 wire net14;
 wire _0347_;
 wire _0348_;
 wire clknet_leaf_32_clk_ref;
 wire _0350_;
 wire _0351_;
 wire _0352_;
 wire _0353_;
 wire clknet_leaf_34_clk_ref;
 wire clknet_leaf_33_clk_ref;
 wire _0356_;
 wire clknet_leaf_36_clk_ref;
 wire clknet_leaf_35_clk_ref;
 wire _0359_;
 wire clknet_2_2__leaf_clk_ref;
 wire clknet_2_1__leaf_clk_ref;
 wire _0362_;
 wire clknet_leaf_38_clk_ref;
 wire clknet_leaf_37_clk_ref;
 wire _0365_;
 wire clknet_2_3__leaf_clk_ref;
 wire _0368_;
 wire _0369_;
 wire _0370_;
 wire _0371_;
 wire _0372_;
 wire _0373_;
 wire _0374_;
 wire _0375_;
 wire _0376_;
 wire _0377_;
 wire _0378_;
 wire _0379_;
 wire _0380_;
 wire _0381_;
 wire clknet_leaf_31_clk_ref;
 wire _0383_;
 wire _0384_;
 wire _0385_;
 wire _0386_;
 wire _0387_;
 wire _0388_;
 wire _0389_;
 wire _0390_;
 wire _0391_;
 wire _0392_;
 wire _0393_;
 wire _0394_;
 wire _0396_;
 wire _0397_;
 wire clknet_leaf_27_clk_ref;
 wire _0399_;
 wire clknet_leaf_26_clk_ref;
 wire _0401_;
 wire _0402_;
 wire _0403_;
 wire _0404_;
 wire _0405_;
 wire _0406_;
 wire _0407_;
 wire _0408_;
 wire _0409_;
 wire _0410_;
 wire _0411_;
 wire _0412_;
 wire _0413_;
 wire _0414_;
 wire _0415_;
 wire _0416_;
 wire _0417_;
 wire _0418_;
 wire _0419_;
 wire _0420_;
 wire _0421_;
 wire _0422_;
 wire _0423_;
 wire _0424_;
 wire _0425_;
 wire _0426_;
 wire _0427_;
 wire _0428_;
 wire _0429_;
 wire _0430_;
 wire _0431_;
 wire _0432_;
 wire _0433_;
 wire _0434_;
 wire _0435_;
 wire _0436_;
 wire _0437_;
 wire _0438_;
 wire _0439_;
 wire _0440_;
 wire _0443_;
 wire _0444_;
 wire _0445_;
 wire _0446_;
 wire _0447_;
 wire clknet_leaf_40_clk_ref;
 wire _0449_;
 wire _0450_;
 wire _0452_;
 wire _0453_;
 wire _0454_;
 wire _0455_;
 wire clknet_leaf_39_clk_ref;
 wire _0458_;
 wire _0459_;
 wire _0460_;
 wire _0461_;
 wire _0462_;
 wire _0463_;
 wire _0464_;
 wire _0465_;
 wire _0466_;
 wire _0467_;
 wire _0468_;
 wire _0469_;
 wire _0470_;
 wire clknet_leaf_15_clk_ref;
 wire _0472_;
 wire clknet_leaf_10_clk_ref;
 wire clknet_leaf_7_clk_ref;
 wire _0475_;
 wire _0476_;
 wire net19;
 wire _0478_;
 wire _0479_;
 wire clknet_leaf_11_clk_ref;
 wire clknet_leaf_1_clk_ref;
 wire _0482_;
 wire _0483_;
 wire clknet_leaf_17_clk_ref;
 wire _0485_;
 wire clknet_leaf_21_clk_ref;
 wire _0487_;
 wire _0488_;
 wire _0489_;
 wire _0490_;
 wire _0491_;
 wire clknet_leaf_22_clk_ref;
 wire _0493_;
 wire clknet_leaf_13_clk_ref;
 wire _0495_;
 wire _0496_;
 wire clknet_leaf_24_clk_ref;
 wire _0498_;
 wire clknet_leaf_6_clk_ref;
 wire _0500_;
 wire clknet_leaf_14_clk_ref;
 wire clknet_leaf_20_clk_ref;
 wire clknet_leaf_18_clk_ref;
 wire _0504_;
 wire _0505_;
 wire _0506_;
 wire net17;
 wire _0508_;
 wire clknet_leaf_9_clk_ref;
 wire clknet_leaf_16_clk_ref;
 wire _0511_;
 wire _0512_;
 wire _0513_;
 wire _0514_;
 wire clknet_leaf_8_clk_ref;
 wire _0516_;
 wire _0517_;
 wire _0518_;
 wire _0519_;
 wire clknet_leaf_0_clk_ref;
 wire _0521_;
 wire _0522_;
 wire _0523_;
 wire _0524_;
 wire _0525_;
 wire _0526_;
 wire _0527_;
 wire net20;
 wire _0529_;
 wire _0530_;
 wire _0531_;
 wire _0532_;
 wire net21;
 wire _0534_;
 wire clknet_leaf_19_clk_ref;
 wire clknet_leaf_12_clk_ref;
 wire _0537_;
 wire _0538_;
 wire _0539_;
 wire _0540_;
 wire _0541_;
 wire _0542_;
 wire _0543_;
 wire _0544_;
 wire _0545_;
 wire _0546_;
 wire _0547_;
 wire clknet_leaf_23_clk_ref;
 wire _0549_;
 wire _0550_;
 wire _0551_;
 wire _0552_;
 wire _0553_;
 wire _0554_;
 wire _0555_;
 wire _0556_;
 wire _0557_;
 wire _0558_;
 wire _0559_;
 wire _0560_;
 wire _0561_;
 wire _0562_;
 wire _0563_;
 wire _0564_;
 wire net16;
 wire _0566_;
 wire _0567_;
 wire _0568_;
 wire _0569_;
 wire _0570_;
 wire _0571_;
 wire _0572_;
 wire _0573_;
 wire _0574_;
 wire _0575_;
 wire _0576_;
 wire _0577_;
 wire _0578_;
 wire _0579_;
 wire _0580_;
 wire _0581_;
 wire _0582_;
 wire _0583_;
 wire _0584_;
 wire _0585_;
 wire _0586_;
 wire _0587_;
 wire _0588_;
 wire _0589_;
 wire _0590_;
 wire _0591_;
 wire _0592_;
 wire _0593_;
 wire _0594_;
 wire _0595_;
 wire _0596_;
 wire _0597_;
 wire _0598_;
 wire _0599_;
 wire _0600_;
 wire _0601_;
 wire _0602_;
 wire _0603_;
 wire _0604_;
 wire _0605_;
 wire _0606_;
 wire _0607_;
 wire _0608_;
 wire _0609_;
 wire _0610_;
 wire _0611_;
 wire _0612_;
 wire _0613_;
 wire _0614_;
 wire _0615_;
 wire _0616_;
 wire _0617_;
 wire _0618_;
 wire _0619_;
 wire _0620_;
 wire _0621_;
 wire _0622_;
 wire _0623_;
 wire _0624_;
 wire _0625_;
 wire _0626_;
 wire _0627_;
 wire _0628_;
 wire _0629_;
 wire _0630_;
 wire _0631_;
 wire _0632_;
 wire _0633_;
 wire _0634_;
 wire _0635_;
 wire _0636_;
 wire _0637_;
 wire _0638_;
 wire _0639_;
 wire _0640_;
 wire _0641_;
 wire _0642_;
 wire _0643_;
 wire _0644_;
 wire _0645_;
 wire _0646_;
 wire _0647_;
 wire _0648_;
 wire clknet_leaf_25_clk_ref;
 wire _0650_;
 wire _0651_;
 wire _0652_;
 wire _0653_;
 wire _0654_;
 wire _0655_;
 wire _0656_;
 wire _0657_;
 wire _0658_;
 wire _0659_;
 wire _0660_;
 wire _0661_;
 wire _0662_;
 wire _0663_;
 wire _0664_;
 wire _0665_;
 wire _0666_;
 wire _0667_;
 wire _0668_;
 wire _0669_;
 wire _0670_;
 wire _0671_;
 wire _0672_;
 wire _0673_;
 wire _0674_;
 wire _0675_;
 wire _0676_;
 wire _0677_;
 wire _0678_;
 wire _0679_;
 wire _0680_;
 wire _0681_;
 wire _0682_;
 wire _0683_;
 wire _0684_;
 wire _0685_;
 wire _0686_;
 wire _0687_;
 wire _0688_;
 wire _0689_;
 wire _0690_;
 wire _0691_;
 wire net15;
 wire net12;
 wire clknet_leaf_3_clk_ref;
 wire _0695_;
 wire _0696_;
 wire clknet_leaf_2_clk_ref;
 wire _0698_;
 wire _0699_;
 wire _0700_;
 wire _0701_;
 wire net13;
 wire net22;
 wire net11;
 wire _0705_;
 wire _0706_;
 wire _0707_;
 wire _0708_;
 wire _0709_;
 wire _0710_;
 wire _0711_;
 wire _0712_;
 wire _0713_;
 wire net10;
 wire _0715_;
 wire _0716_;
 wire _0717_;
 wire _0718_;
 wire _0719_;
 wire _0720_;
 wire _0721_;
 wire _0722_;
 wire _0723_;
 wire _0724_;
 wire _0725_;
 wire _0726_;
 wire _0727_;
 wire _0728_;
 wire _0729_;
 wire _0730_;
 wire _0731_;
 wire _0732_;
 wire _0733_;
 wire _0734_;
 wire _0735_;
 wire _0736_;
 wire _0737_;
 wire _0738_;
 wire _0739_;
 wire _0740_;
 wire _0741_;
 wire _0742_;
 wire _0743_;
 wire _0744_;
 wire _0745_;
 wire _0746_;
 wire _0747_;
 wire _0748_;
 wire _0749_;
 wire _0750_;
 wire _0751_;
 wire _0752_;
 wire _0753_;
 wire _0754_;
 wire _0755_;
 wire _0756_;
 wire _0757_;
 wire _0758_;
 wire _0759_;
 wire _0760_;
 wire _0761_;
 wire _0762_;
 wire _0763_;
 wire _0764_;
 wire _0765_;
 wire _0766_;
 wire _0767_;
 wire _0768_;
 wire _0769_;
 wire _0770_;
 wire _0771_;
 wire _0772_;
 wire busy_r;
 wire done_r;
 wire gate_en;
 wire osc_sel_clk;
 wire ovf_o;
 wire ovf_r;
 wire tog_o;
 wire tog_s1;
 wire tog_s2;
 wire tog_s3;
 wire \u_cnt/_000_ ;
 wire \u_cnt/_001_ ;
 wire \u_cnt/_002_ ;
 wire \u_cnt/_003_ ;
 wire \u_cnt/_004_ ;
 wire \u_cnt/_005_ ;
 wire \u_cnt/_006_ ;
 wire \u_cnt/_007_ ;
 wire \u_cnt/_008_ ;
 wire \u_cnt/_009_ ;
 wire \u_cnt/_010_ ;
 wire \u_cnt/_011_ ;
 wire \u_cnt/_012_ ;
 wire \u_cnt/_013_ ;
 wire \u_cnt/_014_ ;
 wire \u_cnt/_015_ ;
 wire \u_cnt/_016_ ;
 wire \u_cnt/_017_ ;
 wire \u_cnt/_018_ ;
 wire \u_cnt/_019_ ;
 wire \u_cnt/_020_ ;
 wire \u_cnt/_021_ ;
 wire \u_cnt/_022_ ;
 wire \u_cnt/_023_ ;
 wire \u_cnt/_024_ ;
 wire \u_cnt/_025_ ;
 wire \u_cnt/_026_ ;
 wire \u_cnt/_027_ ;
 wire \u_cnt/_028_ ;
 wire \u_cnt/_029_ ;
 wire \u_cnt/_030_ ;
 wire \u_cnt/_031_ ;
 wire \u_cnt/_032_ ;
 wire \u_cnt/_033_ ;
 wire \u_cnt/_034_ ;
 wire \u_cnt/_035_ ;
 wire \u_cnt/_036_ ;
 wire \u_cnt/_037_ ;
 wire \u_cnt/_038_ ;
 wire \u_cnt/_039_ ;
 wire \u_cnt/_040_ ;
 wire \u_cnt/_041_ ;
 wire \u_cnt/_042_ ;
 wire \u_cnt/_043_ ;
 wire \u_cnt/_044_ ;
 wire \u_cnt/_045_ ;
 wire \u_cnt/_046_ ;
 wire \u_cnt/_047_ ;
 wire \u_cnt/_048_ ;
 wire \u_cnt/_049_ ;
 wire \u_cnt/_050_ ;
 wire \u_cnt/_051_ ;
 wire \u_cnt/_052_ ;
 wire \u_cnt/_053_ ;
 wire \u_cnt/_054_ ;
 wire \u_cnt/_055_ ;
 wire \u_cnt/_056_ ;
 wire \u_cnt/_057_ ;
 wire \u_cnt/_058_ ;
 wire \u_cnt/_059_ ;
 wire \u_cnt/_060_ ;
 wire \u_cnt/_061_ ;
 wire \u_cnt/_062_ ;
 wire \u_cnt/_063_ ;
 wire \u_cnt/_064_ ;
 wire \u_cnt/_065_ ;
 wire \u_cnt/_066_ ;
 wire \u_cnt/_067_ ;
 wire \u_cnt/_068_ ;
 wire \u_cnt/_069_ ;
 wire \u_cnt/_070_ ;
 wire \u_cnt/_071_ ;
 wire \u_cnt/_072_ ;
 wire \u_cnt/_073_ ;
 wire \u_cnt/_074_ ;
 wire \u_cnt/_075_ ;
 wire \u_cnt/_076_ ;
 wire \u_cnt/_077_ ;
 wire \u_cnt/_078_ ;
 wire \u_cnt/_079_ ;
 wire \u_cnt/_080_ ;
 wire \u_cnt/_081_ ;
 wire \u_cnt/_082_ ;
 wire \u_cnt/_083_ ;
 wire \u_cnt/_084_ ;
 wire \u_cnt/_086_ ;
 wire \u_cnt/_088_ ;
 wire \u_cnt/_090_ ;
 wire \u_cnt/_093_ ;
 wire \u_cnt/_094_ ;
 wire \u_cnt/_095_ ;
 wire \u_cnt/_096_ ;
 wire \u_cnt/_097_ ;
 wire \u_cnt/_099_ ;
 wire \u_cnt/_100_ ;
 wire \u_cnt/_101_ ;
 wire \u_cnt/_102_ ;
 wire \u_cnt/_103_ ;
 wire \u_cnt/_104_ ;
 wire \u_cnt/_105_ ;
 wire \u_cnt/_106_ ;
 wire \u_cnt/gate_s1 ;
 wire \u_cnt/gate_s2 ;
 wire \u_cnt/running ;
 wire [23:0] \cal_r[0] ;
 wire [23:0] \cal_r[1] ;
 wire [23:0] \cal_r[2] ;
 wire [23:0] \cal_r[3] ;
 wire [23:0] \cal_r[4] ;
 wire [23:0] cnt_o;
 wire [23:0] \count_r[0] ;
 wire [23:0] \count_r[1] ;
 wire [23:0] \count_r[2] ;
 wire [23:0] \count_r[3] ;
 wire [23:0] \count_r[4] ;
 wire [4:0] ctrl_k;
 wire [2:0] ctrl_sel;
 wire [31:0] gate_cnt;
 wire [4:0] k_q;
 wire [2:0] sel_q;

 sky130_fd_sc_hd__diode_2 ANTENNA_1 (.DIODE(clk_ref));
 sky130_fd_sc_hd__diode_2 ANTENNA_2 (.DIODE(osc[3]));
 sky130_fd_sc_hd__buf_2 _0773_ (.A(addr[1]),
    .X(_0466_));
 sky130_fd_sc_hd__clkbuf_1 _0774_ (.A(addr[2]),
    .X(_0467_));
 sky130_fd_sc_hd__buf_2 _0775_ (.A(addr[0]),
    .X(_0468_));
 sky130_fd_sc_hd__a31oi_1 _0776_ (.A1(_0468_),
    .A2(_0466_),
    .A3(_0467_),
    .B1(addr[3]),
    .Y(_0469_));
 sky130_fd_sc_hd__o21ai_1 _0777_ (.A1(_0466_),
    .A2(_0467_),
    .B1(_0469_),
    .Y(_0470_));
 sky130_fd_sc_hd__nor3b_1 _0779_ (.A(_0468_),
    .B(_0466_),
    .C_N(addr[2]),
    .Y(_0472_));
 sky130_fd_sc_hd__nand2_1 _0782_ (.A(_0468_),
    .B(_0466_),
    .Y(_0475_));
 sky130_fd_sc_hd__xor2_1 _0783_ (.A(_0467_),
    .B(_0475_),
    .X(_0476_));
 sky130_fd_sc_hd__nand2_1 _0785_ (.A(\count_r[0] [22]),
    .B(net17),
    .Y(_0478_));
 sky130_fd_sc_hd__and3b_1 _0786_ (.A_N(_0468_),
    .B(_0466_),
    .C(_0467_),
    .X(_0479_));
 sky130_fd_sc_hd__nand2_1 _0789_ (.A(_0468_),
    .B(_0467_),
    .Y(_0482_));
 sky130_fd_sc_hd__nor2_1 _0790_ (.A(_0466_),
    .B(_0482_),
    .Y(_0483_));
 sky130_fd_sc_hd__nor2_1 _0792_ (.A(_0467_),
    .B(_0475_),
    .Y(_0485_));
 sky130_fd_sc_hd__a222oi_1 _0794_ (.A1(\count_r[4] [22]),
    .A2(_0479_),
    .B1(net16),
    .B2(\count_r[3] [22]),
    .C1(\count_r[1] [22]),
    .C2(net14),
    .Y(_0487_));
 sky130_fd_sc_hd__nand2_1 _0795_ (.A(_0478_),
    .B(_0487_),
    .Y(_0488_));
 sky130_fd_sc_hd__a21oi_1 _0796_ (.A1(\count_r[2] [22]),
    .A2(net22),
    .B1(_0488_),
    .Y(_0489_));
 sky130_fd_sc_hd__o21ai_0 _0797_ (.A1(_0468_),
    .A2(addr[1]),
    .B1(addr[2]),
    .Y(_0490_));
 sky130_fd_sc_hd__nand2_1 _0798_ (.A(addr[3]),
    .B(_0490_),
    .Y(_0491_));
 sky130_fd_sc_hd__nor3b_1 _0800_ (.A(_0466_),
    .B(_0467_),
    .C_N(_0468_),
    .Y(_0493_));
 sky130_fd_sc_hd__or3_1 _0802_ (.A(addr[0]),
    .B(addr[1]),
    .C(addr[2]),
    .X(_0495_));
 sky130_fd_sc_hd__nand2_1 _0803_ (.A(_0490_),
    .B(_0495_),
    .Y(_0496_));
 sky130_fd_sc_hd__nand2_1 _0805_ (.A(\cal_r[0] [22]),
    .B(_0496_),
    .Y(_0498_));
 sky130_fd_sc_hd__nor3b_1 _0807_ (.A(_0468_),
    .B(_0467_),
    .C_N(_0466_),
    .Y(_0500_));
 sky130_fd_sc_hd__a222oi_1 _0811_ (.A1(\cal_r[4] [22]),
    .A2(net22),
    .B1(net19),
    .B2(\cal_r[2] [22]),
    .C1(net15),
    .C2(\cal_r[3] [22]),
    .Y(_0504_));
 sky130_fd_sc_hd__nand2_1 _0812_ (.A(_0498_),
    .B(_0504_),
    .Y(_0505_));
 sky130_fd_sc_hd__a21oi_1 _0813_ (.A1(\cal_r[1] [22]),
    .A2(net20),
    .B1(_0505_),
    .Y(_0506_));
 sky130_fd_sc_hd__o22ai_1 _0814_ (.A1(net18),
    .A2(_0489_),
    .B1(_0491_),
    .B2(_0506_),
    .Y(rdata[22]));
 sky130_fd_sc_hd__nand2_1 _0816_ (.A(\count_r[0] [21]),
    .B(net17),
    .Y(_0508_));
 sky130_fd_sc_hd__a222oi_1 _0819_ (.A1(\count_r[2] [21]),
    .A2(net22),
    .B1(_0479_),
    .B2(\count_r[4] [21]),
    .C1(net16),
    .C2(\count_r[3] [21]),
    .Y(_0511_));
 sky130_fd_sc_hd__nand2_1 _0820_ (.A(_0508_),
    .B(_0511_),
    .Y(_0512_));
 sky130_fd_sc_hd__a21oi_1 _0821_ (.A1(\count_r[1] [21]),
    .A2(net15),
    .B1(_0512_),
    .Y(_0513_));
 sky130_fd_sc_hd__nand2_1 _0822_ (.A(\cal_r[0] [21]),
    .B(_0496_),
    .Y(_0514_));
 sky130_fd_sc_hd__a222oi_1 _0824_ (.A1(\cal_r[4] [21]),
    .A2(net21),
    .B1(_0500_),
    .B2(\cal_r[2] [21]),
    .C1(net15),
    .C2(\cal_r[3] [21]),
    .Y(_0516_));
 sky130_fd_sc_hd__nand2_1 _0825_ (.A(_0514_),
    .B(_0516_),
    .Y(_0517_));
 sky130_fd_sc_hd__a21oi_1 _0826_ (.A1(\cal_r[1] [21]),
    .A2(_0493_),
    .B1(_0517_),
    .Y(_0518_));
 sky130_fd_sc_hd__o22ai_1 _0827_ (.A1(_0470_),
    .A2(_0513_),
    .B1(_0518_),
    .B2(_0491_),
    .Y(rdata[21]));
 sky130_fd_sc_hd__nand2_1 _0828_ (.A(\count_r[0] [20]),
    .B(net17),
    .Y(_0519_));
 sky130_fd_sc_hd__a222oi_1 _0830_ (.A1(\count_r[2] [20]),
    .A2(net21),
    .B1(net16),
    .B2(\count_r[3] [20]),
    .C1(_0479_),
    .C2(\count_r[4] [20]),
    .Y(_0521_));
 sky130_fd_sc_hd__nand2_1 _0831_ (.A(_0519_),
    .B(_0521_),
    .Y(_0522_));
 sky130_fd_sc_hd__a21oi_1 _0832_ (.A1(\count_r[1] [20]),
    .A2(net15),
    .B1(_0522_),
    .Y(_0523_));
 sky130_fd_sc_hd__nand2_1 _0833_ (.A(\cal_r[0] [20]),
    .B(_0496_),
    .Y(_0524_));
 sky130_fd_sc_hd__a222oi_1 _0834_ (.A1(\cal_r[4] [20]),
    .A2(net21),
    .B1(_0500_),
    .B2(\cal_r[2] [20]),
    .C1(net15),
    .C2(\cal_r[3] [20]),
    .Y(_0525_));
 sky130_fd_sc_hd__nand2_1 _0835_ (.A(_0524_),
    .B(_0525_),
    .Y(_0526_));
 sky130_fd_sc_hd__a21oi_1 _0836_ (.A1(\cal_r[1] [20]),
    .A2(_0493_),
    .B1(_0526_),
    .Y(_0527_));
 sky130_fd_sc_hd__o22ai_1 _0837_ (.A1(_0470_),
    .A2(_0523_),
    .B1(_0527_),
    .B2(_0491_),
    .Y(rdata[20]));
 sky130_fd_sc_hd__nand2_1 _0839_ (.A(\count_r[0] [19]),
    .B(net17),
    .Y(_0529_));
 sky130_fd_sc_hd__a222oi_1 _0840_ (.A1(\count_r[4] [19]),
    .A2(_0479_),
    .B1(net16),
    .B2(\count_r[3] [19]),
    .C1(\count_r[1] [19]),
    .C2(net15),
    .Y(_0530_));
 sky130_fd_sc_hd__nand2_1 _0841_ (.A(_0529_),
    .B(_0530_),
    .Y(_0531_));
 sky130_fd_sc_hd__a21oi_1 _0842_ (.A1(\count_r[2] [19]),
    .A2(net21),
    .B1(_0531_),
    .Y(_0532_));
 sky130_fd_sc_hd__nand2_1 _0844_ (.A(\cal_r[0] [19]),
    .B(_0496_),
    .Y(_0534_));
 sky130_fd_sc_hd__a222oi_1 _0847_ (.A1(\cal_r[3] [19]),
    .A2(net15),
    .B1(net20),
    .B2(\cal_r[1] [19]),
    .C1(\cal_r[4] [19]),
    .C2(net22),
    .Y(_0537_));
 sky130_fd_sc_hd__nand2_1 _0848_ (.A(_0534_),
    .B(_0537_),
    .Y(_0538_));
 sky130_fd_sc_hd__a21oi_1 _0849_ (.A1(\cal_r[2] [19]),
    .A2(net19),
    .B1(_0538_),
    .Y(_0539_));
 sky130_fd_sc_hd__o22ai_1 _0850_ (.A1(net18),
    .A2(_0532_),
    .B1(_0539_),
    .B2(_0491_),
    .Y(rdata[19]));
 sky130_fd_sc_hd__nand2_1 _0851_ (.A(\cal_r[0] [18]),
    .B(_0496_),
    .Y(_0540_));
 sky130_fd_sc_hd__a222oi_1 _0852_ (.A1(\cal_r[4] [18]),
    .A2(net22),
    .B1(net20),
    .B2(\cal_r[1] [18]),
    .C1(net19),
    .C2(\cal_r[2] [18]),
    .Y(_0541_));
 sky130_fd_sc_hd__nand2_1 _0853_ (.A(_0540_),
    .B(_0541_),
    .Y(_0542_));
 sky130_fd_sc_hd__a21oi_1 _0854_ (.A1(\cal_r[3] [18]),
    .A2(net15),
    .B1(_0542_),
    .Y(_0543_));
 sky130_fd_sc_hd__nand2_1 _0855_ (.A(\count_r[0] [18]),
    .B(net17),
    .Y(_0544_));
 sky130_fd_sc_hd__a222oi_1 _0856_ (.A1(\count_r[2] [18]),
    .A2(net21),
    .B1(_0479_),
    .B2(\count_r[4] [18]),
    .C1(net15),
    .C2(\count_r[1] [18]),
    .Y(_0545_));
 sky130_fd_sc_hd__nand2_1 _0857_ (.A(_0544_),
    .B(_0545_),
    .Y(_0546_));
 sky130_fd_sc_hd__a21oi_1 _0858_ (.A1(\count_r[3] [18]),
    .A2(net16),
    .B1(_0546_),
    .Y(_0547_));
 sky130_fd_sc_hd__o22ai_1 _0859_ (.A1(_0491_),
    .A2(_0543_),
    .B1(_0547_),
    .B2(net18),
    .Y(rdata[18]));
 sky130_fd_sc_hd__nand2_1 _0861_ (.A(\cal_r[0] [17]),
    .B(_0496_),
    .Y(_0549_));
 sky130_fd_sc_hd__a222oi_1 _0862_ (.A1(\cal_r[3] [17]),
    .A2(net15),
    .B1(net19),
    .B2(\cal_r[2] [17]),
    .C1(net20),
    .C2(\cal_r[1] [17]),
    .Y(_0550_));
 sky130_fd_sc_hd__nand2_1 _0863_ (.A(_0549_),
    .B(_0550_),
    .Y(_0551_));
 sky130_fd_sc_hd__a21oi_1 _0864_ (.A1(\cal_r[4] [17]),
    .A2(net22),
    .B1(_0551_),
    .Y(_0552_));
 sky130_fd_sc_hd__nand2_1 _0865_ (.A(\count_r[0] [17]),
    .B(net17),
    .Y(_0553_));
 sky130_fd_sc_hd__a222oi_1 _0866_ (.A1(\count_r[2] [17]),
    .A2(net22),
    .B1(_0479_),
    .B2(\count_r[4] [17]),
    .C1(\count_r[3] [17]),
    .C2(net16),
    .Y(_0554_));
 sky130_fd_sc_hd__nand2_1 _0867_ (.A(_0553_),
    .B(_0554_),
    .Y(_0555_));
 sky130_fd_sc_hd__a21oi_1 _0868_ (.A1(\count_r[1] [17]),
    .A2(net15),
    .B1(_0555_),
    .Y(_0556_));
 sky130_fd_sc_hd__o22ai_1 _0869_ (.A1(_0491_),
    .A2(_0552_),
    .B1(_0556_),
    .B2(net18),
    .Y(rdata[17]));
 sky130_fd_sc_hd__nand2_1 _0870_ (.A(\count_r[0] [16]),
    .B(net17),
    .Y(_0557_));
 sky130_fd_sc_hd__a222oi_1 _0871_ (.A1(\count_r[4] [16]),
    .A2(_0479_),
    .B1(net15),
    .B2(\count_r[1] [16]),
    .C1(net16),
    .C2(\count_r[3] [16]),
    .Y(_0558_));
 sky130_fd_sc_hd__nand2_1 _0872_ (.A(_0557_),
    .B(_0558_),
    .Y(_0559_));
 sky130_fd_sc_hd__a21oi_1 _0873_ (.A1(\count_r[2] [16]),
    .A2(net21),
    .B1(_0559_),
    .Y(_0560_));
 sky130_fd_sc_hd__nand2_1 _0874_ (.A(\cal_r[0] [16]),
    .B(_0496_),
    .Y(_0561_));
 sky130_fd_sc_hd__a222oi_1 _0875_ (.A1(\cal_r[4] [16]),
    .A2(net21),
    .B1(_0500_),
    .B2(\cal_r[2] [16]),
    .C1(net15),
    .C2(\cal_r[3] [16]),
    .Y(_0562_));
 sky130_fd_sc_hd__nand2_1 _0876_ (.A(_0561_),
    .B(_0562_),
    .Y(_0563_));
 sky130_fd_sc_hd__a21oi_1 _0877_ (.A1(\cal_r[1] [16]),
    .A2(_0493_),
    .B1(_0563_),
    .Y(_0564_));
 sky130_fd_sc_hd__o22ai_1 _0878_ (.A1(_0470_),
    .A2(_0560_),
    .B1(_0564_),
    .B2(_0491_),
    .Y(rdata[16]));
 sky130_fd_sc_hd__nand2_1 _0880_ (.A(\cal_r[0] [15]),
    .B(_0496_),
    .Y(_0566_));
 sky130_fd_sc_hd__a222oi_1 _0881_ (.A1(\cal_r[4] [15]),
    .A2(net22),
    .B1(net15),
    .B2(\cal_r[3] [15]),
    .C1(\cal_r[2] [15]),
    .C2(net19),
    .Y(_0567_));
 sky130_fd_sc_hd__nand2_1 _0882_ (.A(_0566_),
    .B(_0567_),
    .Y(_0568_));
 sky130_fd_sc_hd__a21oi_1 _0883_ (.A1(\cal_r[1] [15]),
    .A2(net20),
    .B1(_0568_),
    .Y(_0569_));
 sky130_fd_sc_hd__nand2_1 _0884_ (.A(\count_r[0] [15]),
    .B(net17),
    .Y(_0570_));
 sky130_fd_sc_hd__a222oi_1 _0885_ (.A1(\count_r[4] [15]),
    .A2(_0479_),
    .B1(net16),
    .B2(\count_r[3] [15]),
    .C1(net15),
    .C2(\count_r[1] [15]),
    .Y(_0571_));
 sky130_fd_sc_hd__nand2_1 _0886_ (.A(_0570_),
    .B(_0571_),
    .Y(_0572_));
 sky130_fd_sc_hd__a21oi_1 _0887_ (.A1(\count_r[2] [15]),
    .A2(net21),
    .B1(_0572_),
    .Y(_0573_));
 sky130_fd_sc_hd__o22ai_1 _0888_ (.A1(_0491_),
    .A2(_0569_),
    .B1(_0573_),
    .B2(net18),
    .Y(rdata[15]));
 sky130_fd_sc_hd__nand2_1 _0889_ (.A(\cal_r[0] [14]),
    .B(_0496_),
    .Y(_0574_));
 sky130_fd_sc_hd__a222oi_1 _0890_ (.A1(\cal_r[4] [14]),
    .A2(net21),
    .B1(net15),
    .B2(\cal_r[3] [14]),
    .C1(_0500_),
    .C2(\cal_r[2] [14]),
    .Y(_0575_));
 sky130_fd_sc_hd__nand2_1 _0891_ (.A(_0574_),
    .B(_0575_),
    .Y(_0576_));
 sky130_fd_sc_hd__a21oi_1 _0892_ (.A1(\cal_r[1] [14]),
    .A2(_0493_),
    .B1(_0576_),
    .Y(_0577_));
 sky130_fd_sc_hd__nand2_1 _0893_ (.A(\count_r[0] [14]),
    .B(net17),
    .Y(_0578_));
 sky130_fd_sc_hd__a222oi_1 _0894_ (.A1(\count_r[2] [14]),
    .A2(net21),
    .B1(net15),
    .B2(\count_r[1] [14]),
    .C1(net16),
    .C2(\count_r[3] [14]),
    .Y(_0579_));
 sky130_fd_sc_hd__nand2_1 _0895_ (.A(_0578_),
    .B(_0579_),
    .Y(_0580_));
 sky130_fd_sc_hd__a21oi_1 _0896_ (.A1(\count_r[4] [14]),
    .A2(_0479_),
    .B1(_0580_),
    .Y(_0581_));
 sky130_fd_sc_hd__o22ai_1 _0897_ (.A1(_0491_),
    .A2(_0577_),
    .B1(_0581_),
    .B2(_0470_),
    .Y(rdata[14]));
 sky130_fd_sc_hd__nand2_1 _0898_ (.A(\count_r[0] [13]),
    .B(net17),
    .Y(_0582_));
 sky130_fd_sc_hd__a222oi_1 _0899_ (.A1(\count_r[2] [13]),
    .A2(net21),
    .B1(_0479_),
    .B2(\count_r[4] [13]),
    .C1(net14),
    .C2(\count_r[1] [13]),
    .Y(_0583_));
 sky130_fd_sc_hd__nand2_1 _0900_ (.A(_0582_),
    .B(_0583_),
    .Y(_0584_));
 sky130_fd_sc_hd__a21oi_1 _0901_ (.A1(\count_r[3] [13]),
    .A2(net16),
    .B1(_0584_),
    .Y(_0585_));
 sky130_fd_sc_hd__nand2_1 _0902_ (.A(\cal_r[0] [13]),
    .B(_0496_),
    .Y(_0586_));
 sky130_fd_sc_hd__a222oi_1 _0903_ (.A1(\cal_r[4] [13]),
    .A2(net21),
    .B1(net15),
    .B2(\cal_r[3] [13]),
    .C1(_0493_),
    .C2(\cal_r[1] [13]),
    .Y(_0587_));
 sky130_fd_sc_hd__nand2_1 _0904_ (.A(_0586_),
    .B(_0587_),
    .Y(_0588_));
 sky130_fd_sc_hd__a21oi_1 _0905_ (.A1(\cal_r[2] [13]),
    .A2(_0500_),
    .B1(_0588_),
    .Y(_0589_));
 sky130_fd_sc_hd__o22ai_1 _0906_ (.A1(_0470_),
    .A2(_0585_),
    .B1(_0589_),
    .B2(_0491_),
    .Y(rdata[13]));
 sky130_fd_sc_hd__nand2_1 _0907_ (.A(\count_r[0] [12]),
    .B(_0476_),
    .Y(_0590_));
 sky130_fd_sc_hd__a222oi_1 _0908_ (.A1(\count_r[4] [12]),
    .A2(_0479_),
    .B1(net16),
    .B2(\count_r[3] [12]),
    .C1(net14),
    .C2(\count_r[1] [12]),
    .Y(_0591_));
 sky130_fd_sc_hd__nand2_1 _0909_ (.A(_0590_),
    .B(_0591_),
    .Y(_0592_));
 sky130_fd_sc_hd__a21oi_1 _0910_ (.A1(\count_r[2] [12]),
    .A2(net22),
    .B1(_0592_),
    .Y(_0593_));
 sky130_fd_sc_hd__nand2_1 _0911_ (.A(\cal_r[0] [12]),
    .B(_0496_),
    .Y(_0594_));
 sky130_fd_sc_hd__a222oi_1 _0912_ (.A1(\cal_r[3] [12]),
    .A2(net15),
    .B1(_0500_),
    .B2(\cal_r[2] [12]),
    .C1(_0493_),
    .C2(\cal_r[1] [12]),
    .Y(_0595_));
 sky130_fd_sc_hd__nand2_1 _0913_ (.A(_0594_),
    .B(_0595_),
    .Y(_0596_));
 sky130_fd_sc_hd__a21oi_1 _0914_ (.A1(\cal_r[4] [12]),
    .A2(net22),
    .B1(_0596_),
    .Y(_0597_));
 sky130_fd_sc_hd__o22ai_1 _0915_ (.A1(net18),
    .A2(_0593_),
    .B1(_0597_),
    .B2(_0491_),
    .Y(rdata[12]));
 sky130_fd_sc_hd__nand2_1 _0916_ (.A(\count_r[0] [11]),
    .B(net17),
    .Y(_0598_));
 sky130_fd_sc_hd__a222oi_1 _0917_ (.A1(\count_r[2] [11]),
    .A2(net21),
    .B1(_0479_),
    .B2(\count_r[4] [11]),
    .C1(\count_r[1] [11]),
    .C2(net14),
    .Y(_0599_));
 sky130_fd_sc_hd__nand2_1 _0918_ (.A(_0598_),
    .B(_0599_),
    .Y(_0600_));
 sky130_fd_sc_hd__a21oi_1 _0919_ (.A1(\count_r[3] [11]),
    .A2(net16),
    .B1(_0600_),
    .Y(_0601_));
 sky130_fd_sc_hd__nand2_1 _0920_ (.A(\cal_r[0] [11]),
    .B(_0496_),
    .Y(_0602_));
 sky130_fd_sc_hd__a222oi_1 _0921_ (.A1(\cal_r[4] [11]),
    .A2(net22),
    .B1(net14),
    .B2(\cal_r[3] [11]),
    .C1(net19),
    .C2(\cal_r[2] [11]),
    .Y(_0603_));
 sky130_fd_sc_hd__nand2_1 _0922_ (.A(_0602_),
    .B(_0603_),
    .Y(_0604_));
 sky130_fd_sc_hd__a21oi_1 _0923_ (.A1(\cal_r[1] [11]),
    .A2(net20),
    .B1(_0604_),
    .Y(_0605_));
 sky130_fd_sc_hd__o22ai_1 _0924_ (.A1(net18),
    .A2(_0601_),
    .B1(_0605_),
    .B2(_0491_),
    .Y(rdata[11]));
 sky130_fd_sc_hd__nand2_1 _0925_ (.A(\cal_r[0] [10]),
    .B(_0496_),
    .Y(_0606_));
 sky130_fd_sc_hd__a222oi_1 _0926_ (.A1(\cal_r[4] [10]),
    .A2(net22),
    .B1(net15),
    .B2(\cal_r[3] [10]),
    .C1(net20),
    .C2(\cal_r[1] [10]),
    .Y(_0607_));
 sky130_fd_sc_hd__nand2_1 _0927_ (.A(_0606_),
    .B(_0607_),
    .Y(_0608_));
 sky130_fd_sc_hd__a21oi_1 _0928_ (.A1(\cal_r[2] [10]),
    .A2(net19),
    .B1(_0608_),
    .Y(_0609_));
 sky130_fd_sc_hd__nand2_1 _0929_ (.A(\count_r[0] [10]),
    .B(_0476_),
    .Y(_0610_));
 sky130_fd_sc_hd__a222oi_1 _0930_ (.A1(\count_r[2] [10]),
    .A2(net22),
    .B1(_0479_),
    .B2(\count_r[4] [10]),
    .C1(net16),
    .C2(\count_r[3] [10]),
    .Y(_0611_));
 sky130_fd_sc_hd__nand2_1 _0931_ (.A(_0610_),
    .B(_0611_),
    .Y(_0612_));
 sky130_fd_sc_hd__a21oi_1 _0932_ (.A1(\count_r[1] [10]),
    .A2(net14),
    .B1(_0612_),
    .Y(_0613_));
 sky130_fd_sc_hd__o22ai_1 _0933_ (.A1(_0491_),
    .A2(_0609_),
    .B1(_0613_),
    .B2(net18),
    .Y(rdata[10]));
 sky130_fd_sc_hd__nand2_1 _0934_ (.A(\cal_r[0] [9]),
    .B(_0496_),
    .Y(_0614_));
 sky130_fd_sc_hd__a222oi_1 _0935_ (.A1(\cal_r[3] [9]),
    .A2(net15),
    .B1(_0500_),
    .B2(\cal_r[2] [9]),
    .C1(\cal_r[4] [9]),
    .C2(net21),
    .Y(_0615_));
 sky130_fd_sc_hd__nand2_1 _0936_ (.A(_0614_),
    .B(_0615_),
    .Y(_0616_));
 sky130_fd_sc_hd__a21oi_1 _0937_ (.A1(\cal_r[1] [9]),
    .A2(_0493_),
    .B1(_0616_),
    .Y(_0617_));
 sky130_fd_sc_hd__nand2_1 _0938_ (.A(\count_r[0] [9]),
    .B(net17),
    .Y(_0618_));
 sky130_fd_sc_hd__a222oi_1 _0939_ (.A1(\count_r[2] [9]),
    .A2(net21),
    .B1(_0479_),
    .B2(\count_r[4] [9]),
    .C1(net16),
    .C2(\count_r[3] [9]),
    .Y(_0619_));
 sky130_fd_sc_hd__nand2_1 _0940_ (.A(_0618_),
    .B(_0619_),
    .Y(_0620_));
 sky130_fd_sc_hd__a21oi_1 _0941_ (.A1(\count_r[1] [9]),
    .A2(net14),
    .B1(_0620_),
    .Y(_0621_));
 sky130_fd_sc_hd__o22ai_1 _0942_ (.A1(_0491_),
    .A2(_0617_),
    .B1(_0621_),
    .B2(_0470_),
    .Y(rdata[9]));
 sky130_fd_sc_hd__nand2_1 _0943_ (.A(\cal_r[0] [8]),
    .B(_0496_),
    .Y(_0622_));
 sky130_fd_sc_hd__a222oi_1 _0944_ (.A1(\cal_r[3] [8]),
    .A2(net14),
    .B1(net20),
    .B2(\cal_r[1] [8]),
    .C1(net19),
    .C2(\cal_r[2] [8]),
    .Y(_0623_));
 sky130_fd_sc_hd__nand2_1 _0945_ (.A(_0622_),
    .B(_0623_),
    .Y(_0624_));
 sky130_fd_sc_hd__a21oi_1 _0946_ (.A1(\cal_r[4] [8]),
    .A2(net22),
    .B1(_0624_),
    .Y(_0625_));
 sky130_fd_sc_hd__nor2_4 _0947_ (.A(addr[3]),
    .B(_0495_),
    .Y(_0626_));
 sky130_fd_sc_hd__a22oi_1 _0948_ (.A1(\count_r[2] [8]),
    .A2(net22),
    .B1(net14),
    .B2(\count_r[1] [8]),
    .Y(_0627_));
 sky130_fd_sc_hd__a21oi_1 _0949_ (.A1(_0468_),
    .A2(_0466_),
    .B1(_0467_),
    .Y(_0628_));
 sky130_fd_sc_hd__a222oi_1 _0950_ (.A1(\count_r[0] [8]),
    .A2(_0628_),
    .B1(_0479_),
    .B2(\count_r[4] [8]),
    .C1(net16),
    .C2(\count_r[3] [8]),
    .Y(_0629_));
 sky130_fd_sc_hd__a21oi_1 _0951_ (.A1(_0627_),
    .A2(_0629_),
    .B1(net18),
    .Y(_0630_));
 sky130_fd_sc_hd__a21oi_1 _0952_ (.A1(ctrl_k[4]),
    .A2(_0626_),
    .B1(_0630_),
    .Y(_0631_));
 sky130_fd_sc_hd__o21ai_0 _0953_ (.A1(_0491_),
    .A2(_0625_),
    .B1(_0631_),
    .Y(rdata[8]));
 sky130_fd_sc_hd__a22oi_1 _0954_ (.A1(\cal_r[4] [7]),
    .A2(net22),
    .B1(_0496_),
    .B2(\cal_r[0] [7]),
    .Y(_0632_));
 sky130_fd_sc_hd__a222oi_1 _0955_ (.A1(\cal_r[2] [7]),
    .A2(net19),
    .B1(net20),
    .B2(\cal_r[1] [7]),
    .C1(\cal_r[3] [7]),
    .C2(net14),
    .Y(_0633_));
 sky130_fd_sc_hd__a21oi_1 _0956_ (.A1(_0632_),
    .A2(_0633_),
    .B1(_0491_),
    .Y(_0634_));
 sky130_fd_sc_hd__a22oi_1 _0957_ (.A1(\count_r[2] [7]),
    .A2(net22),
    .B1(net14),
    .B2(\count_r[1] [7]),
    .Y(_0635_));
 sky130_fd_sc_hd__a222oi_1 _0958_ (.A1(\count_r[0] [7]),
    .A2(_0628_),
    .B1(_0479_),
    .B2(\count_r[4] [7]),
    .C1(net16),
    .C2(\count_r[3] [7]),
    .Y(_0636_));
 sky130_fd_sc_hd__a21oi_1 _0959_ (.A1(_0635_),
    .A2(_0636_),
    .B1(net18),
    .Y(_0637_));
 sky130_fd_sc_hd__a211o_1 _0960_ (.A1(ctrl_k[3]),
    .A2(_0626_),
    .B1(_0634_),
    .C1(_0637_),
    .X(rdata[7]));
 sky130_fd_sc_hd__a22oi_1 _0961_ (.A1(\count_r[0] [6]),
    .A2(_0476_),
    .B1(_0479_),
    .B2(\count_r[4] [6]),
    .Y(_0638_));
 sky130_fd_sc_hd__a222oi_1 _0962_ (.A1(\count_r[2] [6]),
    .A2(net22),
    .B1(net14),
    .B2(\count_r[1] [6]),
    .C1(net16),
    .C2(\count_r[3] [6]),
    .Y(_0639_));
 sky130_fd_sc_hd__a21oi_1 _0963_ (.A1(_0638_),
    .A2(_0639_),
    .B1(net18),
    .Y(_0640_));
 sky130_fd_sc_hd__a22oi_1 _0964_ (.A1(\cal_r[0] [6]),
    .A2(_0496_),
    .B1(net19),
    .B2(\cal_r[2] [6]),
    .Y(_0641_));
 sky130_fd_sc_hd__a222oi_1 _0965_ (.A1(\cal_r[4] [6]),
    .A2(net22),
    .B1(net20),
    .B2(\cal_r[1] [6]),
    .C1(net14),
    .C2(\cal_r[3] [6]),
    .Y(_0642_));
 sky130_fd_sc_hd__a21oi_1 _0966_ (.A1(_0641_),
    .A2(_0642_),
    .B1(_0491_),
    .Y(_0643_));
 sky130_fd_sc_hd__a211o_1 _0967_ (.A1(ctrl_k[2]),
    .A2(_0626_),
    .B1(_0640_),
    .C1(_0643_),
    .X(rdata[6]));
 sky130_fd_sc_hd__nand2_1 _0968_ (.A(\cal_r[0] [5]),
    .B(_0496_),
    .Y(_0644_));
 sky130_fd_sc_hd__nand2_1 _0969_ (.A(\cal_r[2] [5]),
    .B(net19),
    .Y(_0645_));
 sky130_fd_sc_hd__a222oi_1 _0970_ (.A1(\cal_r[4] [5]),
    .A2(net22),
    .B1(net15),
    .B2(\cal_r[3] [5]),
    .C1(net20),
    .C2(\cal_r[1] [5]),
    .Y(_0646_));
 sky130_fd_sc_hd__nand3_1 _0971_ (.A(_0644_),
    .B(_0645_),
    .C(_0646_),
    .Y(_0647_));
 sky130_fd_sc_hd__and2_1 _0972_ (.A(addr[3]),
    .B(_0490_),
    .X(_0648_));
 sky130_fd_sc_hd__a22oi_1 _0974_ (.A1(\count_r[0] [5]),
    .A2(net17),
    .B1(net16),
    .B2(\count_r[3] [5]),
    .Y(_0650_));
 sky130_fd_sc_hd__a222oi_1 _0975_ (.A1(\count_r[2] [5]),
    .A2(net22),
    .B1(_0479_),
    .B2(\count_r[4] [5]),
    .C1(net14),
    .C2(\count_r[1] [5]),
    .Y(_0651_));
 sky130_fd_sc_hd__a21oi_1 _0976_ (.A1(_0650_),
    .A2(_0651_),
    .B1(net18),
    .Y(_0652_));
 sky130_fd_sc_hd__a221o_1 _0977_ (.A1(ctrl_k[1]),
    .A2(_0626_),
    .B1(_0647_),
    .B2(_0648_),
    .C1(_0652_),
    .X(rdata[5]));
 sky130_fd_sc_hd__nand2_1 _0978_ (.A(\cal_r[0] [4]),
    .B(_0496_),
    .Y(_0653_));
 sky130_fd_sc_hd__a222oi_1 _0979_ (.A1(\cal_r[4] [4]),
    .A2(net22),
    .B1(net14),
    .B2(\cal_r[3] [4]),
    .C1(net19),
    .C2(\cal_r[2] [4]),
    .Y(_0654_));
 sky130_fd_sc_hd__nand2_1 _0980_ (.A(_0653_),
    .B(_0654_),
    .Y(_0655_));
 sky130_fd_sc_hd__a21oi_1 _0981_ (.A1(\cal_r[1] [4]),
    .A2(net20),
    .B1(_0655_),
    .Y(_0656_));
 sky130_fd_sc_hd__a22oi_1 _0982_ (.A1(\count_r[2] [4]),
    .A2(net22),
    .B1(net14),
    .B2(\count_r[1] [4]),
    .Y(_0657_));
 sky130_fd_sc_hd__a222oi_1 _0983_ (.A1(\count_r[0] [4]),
    .A2(_0628_),
    .B1(_0479_),
    .B2(\count_r[4] [4]),
    .C1(net16),
    .C2(\count_r[3] [4]),
    .Y(_0658_));
 sky130_fd_sc_hd__a21oi_1 _0984_ (.A1(_0657_),
    .A2(_0658_),
    .B1(net18),
    .Y(_0659_));
 sky130_fd_sc_hd__a21oi_1 _0985_ (.A1(ctrl_k[0]),
    .A2(_0626_),
    .B1(_0659_),
    .Y(_0660_));
 sky130_fd_sc_hd__o21ai_0 _0986_ (.A1(_0491_),
    .A2(_0656_),
    .B1(_0660_),
    .Y(rdata[4]));
 sky130_fd_sc_hd__a22oi_1 _0987_ (.A1(\cal_r[0] [3]),
    .A2(_0496_),
    .B1(net20),
    .B2(\cal_r[1] [3]),
    .Y(_0661_));
 sky130_fd_sc_hd__a222oi_1 _0988_ (.A1(\cal_r[4] [3]),
    .A2(net22),
    .B1(net14),
    .B2(\cal_r[3] [3]),
    .C1(net19),
    .C2(\cal_r[2] [3]),
    .Y(_0662_));
 sky130_fd_sc_hd__a21oi_1 _0989_ (.A1(_0661_),
    .A2(_0662_),
    .B1(_0491_),
    .Y(_0663_));
 sky130_fd_sc_hd__a22oi_1 _0990_ (.A1(\count_r[2] [3]),
    .A2(net22),
    .B1(_0479_),
    .B2(\count_r[4] [3]),
    .Y(_0664_));
 sky130_fd_sc_hd__a222oi_1 _0991_ (.A1(\count_r[0] [3]),
    .A2(_0628_),
    .B1(net16),
    .B2(\count_r[3] [3]),
    .C1(net14),
    .C2(\count_r[1] [3]),
    .Y(_0665_));
 sky130_fd_sc_hd__a21oi_1 _0992_ (.A1(_0664_),
    .A2(_0665_),
    .B1(net18),
    .Y(_0666_));
 sky130_fd_sc_hd__a211o_1 _0993_ (.A1(ctrl_sel[2]),
    .A2(_0626_),
    .B1(_0663_),
    .C1(_0666_),
    .X(rdata[3]));
 sky130_fd_sc_hd__nor2b_1 _0994_ (.A(addr[3]),
    .B_N(net20),
    .Y(_0667_));
 sky130_fd_sc_hd__a22oi_1 _0995_ (.A1(\count_r[0] [2]),
    .A2(_0628_),
    .B1(_0479_),
    .B2(\count_r[4] [2]),
    .Y(_0668_));
 sky130_fd_sc_hd__a222oi_1 _0996_ (.A1(\count_r[2] [2]),
    .A2(net22),
    .B1(net16),
    .B2(\count_r[3] [2]),
    .C1(net14),
    .C2(\count_r[1] [2]),
    .Y(_0669_));
 sky130_fd_sc_hd__a21oi_1 _0997_ (.A1(_0668_),
    .A2(_0669_),
    .B1(net18),
    .Y(_0670_));
 sky130_fd_sc_hd__a21oi_1 _0998_ (.A1(ovf_r),
    .A2(_0667_),
    .B1(_0670_),
    .Y(_0671_));
 sky130_fd_sc_hd__nand2_1 _0999_ (.A(\cal_r[0] [2]),
    .B(_0496_),
    .Y(_0672_));
 sky130_fd_sc_hd__nand2_1 _1000_ (.A(\cal_r[3] [2]),
    .B(net15),
    .Y(_0673_));
 sky130_fd_sc_hd__a222oi_1 _1001_ (.A1(\cal_r[4] [2]),
    .A2(net22),
    .B1(net19),
    .B2(\cal_r[2] [2]),
    .C1(\cal_r[1] [2]),
    .C2(net20),
    .Y(_0674_));
 sky130_fd_sc_hd__a31oi_1 _1002_ (.A1(_0672_),
    .A2(_0673_),
    .A3(_0674_),
    .B1(_0491_),
    .Y(_0675_));
 sky130_fd_sc_hd__a21oi_1 _1003_ (.A1(ctrl_sel[1]),
    .A2(_0626_),
    .B1(_0675_),
    .Y(_0676_));
 sky130_fd_sc_hd__nand2_1 _1004_ (.A(_0671_),
    .B(_0676_),
    .Y(rdata[2]));
 sky130_fd_sc_hd__a22oi_1 _1005_ (.A1(\count_r[3] [1]),
    .A2(net16),
    .B1(net14),
    .B2(\count_r[1] [1]),
    .Y(_0677_));
 sky130_fd_sc_hd__a222oi_1 _1006_ (.A1(\count_r[0] [1]),
    .A2(_0628_),
    .B1(net22),
    .B2(\count_r[2] [1]),
    .C1(_0479_),
    .C2(\count_r[4] [1]),
    .Y(_0678_));
 sky130_fd_sc_hd__a21oi_1 _1007_ (.A1(_0677_),
    .A2(_0678_),
    .B1(net18),
    .Y(_0679_));
 sky130_fd_sc_hd__a21oi_1 _1008_ (.A1(done_r),
    .A2(_0667_),
    .B1(_0679_),
    .Y(_0680_));
 sky130_fd_sc_hd__a22oi_1 _1009_ (.A1(\cal_r[3] [1]),
    .A2(net15),
    .B1(_0496_),
    .B2(\cal_r[0] [1]),
    .Y(_0681_));
 sky130_fd_sc_hd__a222oi_1 _1010_ (.A1(\cal_r[4] [1]),
    .A2(net22),
    .B1(net20),
    .B2(\cal_r[1] [1]),
    .C1(net19),
    .C2(\cal_r[2] [1]),
    .Y(_0682_));
 sky130_fd_sc_hd__a21oi_1 _1011_ (.A1(_0681_),
    .A2(_0682_),
    .B1(_0491_),
    .Y(_0683_));
 sky130_fd_sc_hd__a21oi_1 _1012_ (.A1(ctrl_sel[0]),
    .A2(_0626_),
    .B1(_0683_),
    .Y(_0684_));
 sky130_fd_sc_hd__nand2_1 _1013_ (.A(_0680_),
    .B(_0684_),
    .Y(rdata[1]));
 sky130_fd_sc_hd__nand2_1 _1014_ (.A(\cal_r[0] [0]),
    .B(_0496_),
    .Y(_0685_));
 sky130_fd_sc_hd__nand2_1 _1015_ (.A(\cal_r[3] [0]),
    .B(net15),
    .Y(_0686_));
 sky130_fd_sc_hd__a222oi_1 _1016_ (.A1(\cal_r[4] [0]),
    .A2(net22),
    .B1(net19),
    .B2(\cal_r[2] [0]),
    .C1(\cal_r[1] [0]),
    .C2(net20),
    .Y(_0687_));
 sky130_fd_sc_hd__nand3_1 _1017_ (.A(_0685_),
    .B(_0686_),
    .C(_0687_),
    .Y(_0688_));
 sky130_fd_sc_hd__a22oi_1 _1018_ (.A1(\count_r[0] [0]),
    .A2(_0476_),
    .B1(net16),
    .B2(\count_r[3] [0]),
    .Y(_0689_));
 sky130_fd_sc_hd__a222oi_1 _1019_ (.A1(\count_r[2] [0]),
    .A2(net22),
    .B1(_0479_),
    .B2(\count_r[4] [0]),
    .C1(net14),
    .C2(\count_r[1] [0]),
    .Y(_0690_));
 sky130_fd_sc_hd__a21oi_1 _1020_ (.A1(_0689_),
    .A2(_0690_),
    .B1(net18),
    .Y(_0691_));
 sky130_fd_sc_hd__a221o_1 _1021_ (.A1(busy_r),
    .A2(_0667_),
    .B1(_0688_),
    .B2(_0648_),
    .C1(_0691_),
    .X(rdata[0]));
 sky130_fd_sc_hd__a21oi_1 _1025_ (.A1(k_q[3]),
    .A2(k_q[2]),
    .B1(k_q[4]),
    .Y(_0695_));
 sky130_fd_sc_hd__xor2_1 _1026_ (.A(gate_cnt[11]),
    .B(_0695_),
    .X(_0696_));
 sky130_fd_sc_hd__or3_1 _1028_ (.A(k_q[3]),
    .B(k_q[2]),
    .C(k_q[1]),
    .X(_0698_));
 sky130_fd_sc_hd__nand2_1 _1029_ (.A(k_q[4]),
    .B(_0698_),
    .Y(_0699_));
 sky130_fd_sc_hd__xor2_1 _1030_ (.A(gate_cnt[17]),
    .B(_0699_),
    .X(_0700_));
 sky130_fd_sc_hd__inv_1 _1031_ (.A(gate_cnt[29]),
    .Y(_0701_));
 sky130_fd_sc_hd__and2_1 _1035_ (.A(k_q[2]),
    .B(k_q[1]),
    .X(_0705_));
 sky130_fd_sc_hd__nand3_1 _1036_ (.A(k_q[3]),
    .B(k_q[4]),
    .C(_0705_),
    .Y(_0706_));
 sky130_fd_sc_hd__xnor2_1 _1037_ (.A(_0701_),
    .B(_0706_),
    .Y(_0707_));
 sky130_fd_sc_hd__a21oi_1 _1038_ (.A1(k_q[3]),
    .A2(_0705_),
    .B1(k_q[4]),
    .Y(_0708_));
 sky130_fd_sc_hd__xor2_1 _1039_ (.A(gate_cnt[13]),
    .B(_0708_),
    .X(_0709_));
 sky130_fd_sc_hd__nand4_1 _1040_ (.A(_0696_),
    .B(_0700_),
    .C(_0707_),
    .D(_0709_),
    .Y(_0710_));
 sky130_fd_sc_hd__o21ai_0 _1041_ (.A1(k_q[3]),
    .A2(_0705_),
    .B1(k_q[4]),
    .Y(_0711_));
 sky130_fd_sc_hd__xnor2_1 _1042_ (.A(gate_cnt[21]),
    .B(_0711_),
    .Y(_0712_));
 sky130_fd_sc_hd__nor2_1 _1043_ (.A(k_q[4]),
    .B(_0698_),
    .Y(_0713_));
 sky130_fd_sc_hd__a211oi_1 _1045_ (.A1(k_q[1]),
    .A2(k_q[0]),
    .B1(k_q[3]),
    .C1(k_q[2]),
    .Y(_0715_));
 sky130_fd_sc_hd__nor2b_1 _1046_ (.A(k_q[4]),
    .B_N(_0715_),
    .Y(_0716_));
 sky130_fd_sc_hd__nand3_1 _1047_ (.A(k_q[3]),
    .B(k_q[2]),
    .C(k_q[4]),
    .Y(_0717_));
 sky130_fd_sc_hd__xor2_1 _1048_ (.A(gate_cnt[27]),
    .B(_0717_),
    .X(_0718_));
 sky130_fd_sc_hd__o221ai_1 _1049_ (.A1(gate_cnt[1]),
    .A2(_0713_),
    .B1(_0716_),
    .B2(gate_cnt[2]),
    .C1(_0718_),
    .Y(_0719_));
 sky130_fd_sc_hd__nor3_1 _1050_ (.A(_0710_),
    .B(_0712_),
    .C(_0719_),
    .Y(_0720_));
 sky130_fd_sc_hd__or2_2 _1051_ (.A(k_q[3]),
    .B(k_q[4]),
    .X(_0721_));
 sky130_fd_sc_hd__a21oi_1 _1052_ (.A1(k_q[0]),
    .A2(_0705_),
    .B1(_0721_),
    .Y(_0722_));
 sky130_fd_sc_hd__nand4bb_1 _1053_ (.A_N(k_q[2]),
    .B_N(k_q[0]),
    .C(k_q[1]),
    .D(k_q[3]),
    .Y(_0723_));
 sky130_fd_sc_hd__nand2_1 _1054_ (.A(gate_cnt[25]),
    .B(_0723_),
    .Y(_0724_));
 sky130_fd_sc_hd__xor2_1 _1055_ (.A(gate_cnt[26]),
    .B(_0724_),
    .X(_0725_));
 sky130_fd_sc_hd__o21ai_0 _1056_ (.A1(k_q[4]),
    .A2(_0723_),
    .B1(gate_cnt[9]),
    .Y(_0726_));
 sky130_fd_sc_hd__xor2_1 _1057_ (.A(gate_cnt[10]),
    .B(_0726_),
    .X(_0727_));
 sky130_fd_sc_hd__nor2_1 _1058_ (.A(k_q[3]),
    .B(k_q[4]),
    .Y(_0728_));
 sky130_fd_sc_hd__nor2_1 _1059_ (.A(gate_cnt[7]),
    .B(_0728_),
    .Y(_0729_));
 sky130_fd_sc_hd__nand2_1 _1060_ (.A(k_q[2]),
    .B(k_q[1]),
    .Y(_0730_));
 sky130_fd_sc_hd__a21oi_1 _1061_ (.A1(_0728_),
    .A2(_0730_),
    .B1(gate_cnt[5]),
    .Y(_0731_));
 sky130_fd_sc_hd__nand2_1 _1062_ (.A(gate_cnt[7]),
    .B(_0728_),
    .Y(_0732_));
 sky130_fd_sc_hd__nand2_1 _1063_ (.A(k_q[3]),
    .B(k_q[4]),
    .Y(_0733_));
 sky130_fd_sc_hd__xor2_1 _1064_ (.A(gate_cnt[23]),
    .B(_0733_),
    .X(_0734_));
 sky130_fd_sc_hd__nand2_1 _1065_ (.A(_0732_),
    .B(_0734_),
    .Y(_0735_));
 sky130_fd_sc_hd__nor4_1 _1066_ (.A(gate_cnt[31]),
    .B(_0729_),
    .C(_0731_),
    .D(_0735_),
    .Y(_0736_));
 sky130_fd_sc_hd__o2111ai_1 _1067_ (.A1(gate_cnt[6]),
    .A2(_0722_),
    .B1(_0725_),
    .C1(_0727_),
    .D1(_0736_),
    .Y(_0737_));
 sky130_fd_sc_hd__a31oi_1 _1068_ (.A1(k_q[3]),
    .A2(k_q[0]),
    .A3(_0705_),
    .B1(k_q[4]),
    .Y(_0738_));
 sky130_fd_sc_hd__xnor2_1 _1069_ (.A(gate_cnt[14]),
    .B(_0738_),
    .Y(_0739_));
 sky130_fd_sc_hd__o211ai_1 _1070_ (.A1(k_q[2]),
    .A2(k_q[1]),
    .B1(k_q[4]),
    .C1(k_q[3]),
    .Y(_0740_));
 sky130_fd_sc_hd__nor2_1 _1071_ (.A(k_q[1]),
    .B(k_q[0]),
    .Y(_0741_));
 sky130_fd_sc_hd__nor2_1 _1072_ (.A(_0741_),
    .B(_0717_),
    .Y(_0742_));
 sky130_fd_sc_hd__xnor2_1 _1073_ (.A(gate_cnt[28]),
    .B(_0742_),
    .Y(_0743_));
 sky130_fd_sc_hd__o21ai_0 _1074_ (.A1(gate_cnt[25]),
    .A2(_0740_),
    .B1(_0743_),
    .Y(_0744_));
 sky130_fd_sc_hd__or3_1 _1075_ (.A(k_q[2]),
    .B(k_q[1]),
    .C(k_q[0]),
    .X(_0745_));
 sky130_fd_sc_hd__a21oi_1 _1076_ (.A1(k_q[3]),
    .A2(_0745_),
    .B1(k_q[4]),
    .Y(_0746_));
 sky130_fd_sc_hd__nor3_1 _1077_ (.A(k_q[1]),
    .B(k_q[0]),
    .C(k_q[4]),
    .Y(_0747_));
 sky130_fd_sc_hd__nor2_1 _1078_ (.A(_0695_),
    .B(_0747_),
    .Y(_0748_));
 sky130_fd_sc_hd__xnor2_1 _1079_ (.A(gate_cnt[12]),
    .B(_0748_),
    .Y(_0749_));
 sky130_fd_sc_hd__o21ai_0 _1080_ (.A1(k_q[3]),
    .A2(_0745_),
    .B1(k_q[4]),
    .Y(_0750_));
 sky130_fd_sc_hd__xor2_1 _1081_ (.A(gate_cnt[16]),
    .B(_0750_),
    .X(_0751_));
 sky130_fd_sc_hd__a22oi_1 _1082_ (.A1(gate_cnt[8]),
    .A2(_0746_),
    .B1(_0740_),
    .B2(gate_cnt[25]),
    .Y(_0752_));
 sky130_fd_sc_hd__o2111ai_1 _1083_ (.A1(gate_cnt[8]),
    .A2(_0746_),
    .B1(_0749_),
    .C1(_0751_),
    .D1(_0752_),
    .Y(_0753_));
 sky130_fd_sc_hd__o21ai_0 _1084_ (.A1(k_q[0]),
    .A2(_0706_),
    .B1(gate_cnt[29]),
    .Y(_0754_));
 sky130_fd_sc_hd__nor2_1 _1085_ (.A(k_q[3]),
    .B(k_q[0]),
    .Y(_0755_));
 sky130_fd_sc_hd__o21ai_0 _1086_ (.A1(_0755_),
    .A2(_0711_),
    .B1(gate_cnt[22]),
    .Y(_0756_));
 sky130_fd_sc_hd__inv_1 _1087_ (.A(gate_cnt[2]),
    .Y(_0757_));
 sky130_fd_sc_hd__xnor2_1 _1088_ (.A(k_q[4]),
    .B(_0715_),
    .Y(_0758_));
 sky130_fd_sc_hd__o21a_1 _1089_ (.A1(k_q[1]),
    .A2(k_q[0]),
    .B1(k_q[2]),
    .X(_0759_));
 sky130_fd_sc_hd__nor2_1 _1090_ (.A(_0721_),
    .B(_0759_),
    .Y(_0760_));
 sky130_fd_sc_hd__o32a_1 _1091_ (.A1(_0757_),
    .A2(gate_cnt[18]),
    .A3(_0758_),
    .B1(_0760_),
    .B2(gate_cnt[4]),
    .X(_0761_));
 sky130_fd_sc_hd__o21ai_0 _1092_ (.A1(k_q[2]),
    .A2(k_q[1]),
    .B1(k_q[3]),
    .Y(_0762_));
 sky130_fd_sc_hd__nand2b_1 _1093_ (.A_N(k_q[4]),
    .B(_0762_),
    .Y(_0763_));
 sky130_fd_sc_hd__xnor2_1 _1094_ (.A(gate_cnt[9]),
    .B(_0763_),
    .Y(_0764_));
 sky130_fd_sc_hd__o2111ai_1 _1095_ (.A1(gate_cnt[30]),
    .A2(_0754_),
    .B1(_0756_),
    .C1(_0761_),
    .D1(_0764_),
    .Y(_0765_));
 sky130_fd_sc_hd__nor4_1 _1096_ (.A(_0739_),
    .B(_0744_),
    .C(_0753_),
    .D(_0765_),
    .Y(_0766_));
 sky130_fd_sc_hd__inv_1 _1097_ (.A(gate_cnt[22]),
    .Y(_0767_));
 sky130_fd_sc_hd__o21bai_1 _1098_ (.A1(_0755_),
    .A2(_0711_),
    .B1_N(_0722_),
    .Y(_0768_));
 sky130_fd_sc_hd__o21a_1 _1099_ (.A1(k_q[3]),
    .A2(_0759_),
    .B1(k_q[4]),
    .X(_0769_));
 sky130_fd_sc_hd__o21ai_0 _1100_ (.A1(_0760_),
    .A2(_0769_),
    .B1(gate_cnt[4]),
    .Y(_0770_));
 sky130_fd_sc_hd__nor2_1 _1101_ (.A(gate_cnt[20]),
    .B(_0770_),
    .Y(_0771_));
 sky130_fd_sc_hd__nor2_1 _1103_ (.A(k_q[3]),
    .B(k_q[2]),
    .Y(_0293_));
 sky130_fd_sc_hd__nand3_1 _1104_ (.A(gate_cnt[0]),
    .B(_0741_),
    .C(_0293_),
    .Y(_0294_));
 sky130_fd_sc_hd__nor3_1 _1105_ (.A(k_q[3]),
    .B(k_q[2]),
    .C(k_q[1]),
    .Y(_0295_));
 sky130_fd_sc_hd__a211oi_1 _1106_ (.A1(gate_cnt[1]),
    .A2(_0295_),
    .B1(k_q[4]),
    .C1(gate_cnt[15]),
    .Y(_0296_));
 sky130_fd_sc_hd__a32oi_1 _1107_ (.A1(gate_cnt[0]),
    .A2(gate_cnt[15]),
    .A3(k_q[4]),
    .B1(_0294_),
    .B2(_0296_),
    .Y(_0297_));
 sky130_fd_sc_hd__a311oi_1 _1108_ (.A1(gate_cnt[6]),
    .A2(_0767_),
    .A3(_0768_),
    .B1(_0771_),
    .C1(_0297_),
    .Y(_0298_));
 sky130_fd_sc_hd__nand3_1 _1110_ (.A(k_q[3]),
    .B(k_q[4]),
    .C(_0745_),
    .Y(_0300_));
 sky130_fd_sc_hd__o311ai_0 _1111_ (.A1(k_q[3]),
    .A2(k_q[2]),
    .A3(k_q[0]),
    .B1(k_q[4]),
    .C1(_0698_),
    .Y(_0301_));
 sky130_fd_sc_hd__o21ai_0 _1112_ (.A1(k_q[3]),
    .A2(_0759_),
    .B1(k_q[4]),
    .Y(_0302_));
 sky130_fd_sc_hd__o21ai_0 _1113_ (.A1(k_q[3]),
    .A2(k_q[2]),
    .B1(k_q[4]),
    .Y(_0303_));
 sky130_fd_sc_hd__xnor2_1 _1114_ (.A(gate_cnt[19]),
    .B(_0303_),
    .Y(_0304_));
 sky130_fd_sc_hd__a221oi_1 _1115_ (.A1(gate_cnt[18]),
    .A2(_0301_),
    .B1(_0302_),
    .B2(gate_cnt[20]),
    .C1(_0304_),
    .Y(_0305_));
 sky130_fd_sc_hd__o21ai_0 _1116_ (.A1(gate_cnt[24]),
    .A2(_0300_),
    .B1(_0305_),
    .Y(_0306_));
 sky130_fd_sc_hd__nor2_1 _1117_ (.A(k_q[2]),
    .B(_0721_),
    .Y(_0307_));
 sky130_fd_sc_hd__xor2_1 _1118_ (.A(gate_cnt[3]),
    .B(_0307_),
    .X(_0308_));
 sky130_fd_sc_hd__a21oi_1 _1119_ (.A1(_0741_),
    .A2(_0293_),
    .B1(gate_cnt[0]),
    .Y(_0309_));
 sky130_fd_sc_hd__a31oi_1 _1120_ (.A1(gate_cnt[5]),
    .A2(_0728_),
    .A3(_0730_),
    .B1(_0309_),
    .Y(_0310_));
 sky130_fd_sc_hd__nand2_1 _1121_ (.A(gate_cnt[24]),
    .B(_0300_),
    .Y(_0311_));
 sky130_fd_sc_hd__nand3_1 _1122_ (.A(_0308_),
    .B(_0310_),
    .C(_0311_),
    .Y(_0312_));
 sky130_fd_sc_hd__nand2_2 _1123_ (.A(we),
    .B(_0626_),
    .Y(_0313_));
 sky130_fd_sc_hd__o21ai_0 _1124_ (.A1(wdata[1]),
    .A2(wdata[2]),
    .B1(wdata[3]),
    .Y(_0314_));
 sky130_fd_sc_hd__nor4bb_1 _1125_ (.A(busy_r),
    .B(_0313_),
    .C_N(_0314_),
    .D_N(wdata[0]),
    .Y(_0315_));
 sky130_fd_sc_hd__a2111oi_0 _1127_ (.A1(gate_cnt[30]),
    .A2(_0754_),
    .B1(_0306_),
    .C1(_0312_),
    .D1(net13),
    .Y(_0317_));
 sky130_fd_sc_hd__and4b_1 _1128_ (.A_N(_0737_),
    .B(_0766_),
    .C(_0298_),
    .D(_0317_),
    .X(_0318_));
 sky130_fd_sc_hd__nor2_1 _1130_ (.A(gate_en),
    .B(net13),
    .Y(_0320_));
 sky130_fd_sc_hd__a21oi_1 _1131_ (.A1(_0720_),
    .A2(_0318_),
    .B1(_0320_),
    .Y(_0000_));
 sky130_fd_sc_hd__nand2_1 _1132_ (.A(\cal_r[0] [23]),
    .B(_0496_),
    .Y(_0321_));
 sky130_fd_sc_hd__a222oi_1 _1133_ (.A1(\cal_r[3] [23]),
    .A2(net15),
    .B1(_0493_),
    .B2(\cal_r[1] [23]),
    .C1(_0500_),
    .C2(\cal_r[2] [23]),
    .Y(_0322_));
 sky130_fd_sc_hd__nand2_1 _1134_ (.A(_0321_),
    .B(_0322_),
    .Y(_0323_));
 sky130_fd_sc_hd__a21oi_1 _1135_ (.A1(\cal_r[4] [23]),
    .A2(net21),
    .B1(_0323_),
    .Y(_0324_));
 sky130_fd_sc_hd__nand2_1 _1136_ (.A(\count_r[0] [23]),
    .B(net17),
    .Y(_0325_));
 sky130_fd_sc_hd__a222oi_1 _1137_ (.A1(\count_r[2] [23]),
    .A2(net21),
    .B1(net16),
    .B2(\count_r[3] [23]),
    .C1(net14),
    .C2(\count_r[1] [23]),
    .Y(_0326_));
 sky130_fd_sc_hd__nand2_1 _1138_ (.A(_0325_),
    .B(_0326_),
    .Y(_0327_));
 sky130_fd_sc_hd__a21oi_1 _1139_ (.A1(\count_r[4] [23]),
    .A2(_0479_),
    .B1(_0327_),
    .Y(_0328_));
 sky130_fd_sc_hd__o22ai_1 _1140_ (.A1(_0491_),
    .A2(_0324_),
    .B1(_0328_),
    .B2(_0470_),
    .Y(rdata[23]));
 sky130_fd_sc_hd__nor2_1 _1142_ (.A(sel_q[0]),
    .B(sel_q[2]),
    .Y(_0330_));
 sky130_fd_sc_hd__nand3_1 _1143_ (.A(sel_q[1]),
    .B(osc[2]),
    .C(_0330_),
    .Y(_0331_));
 sky130_fd_sc_hd__nor3_1 _1144_ (.A(sel_q[0]),
    .B(sel_q[2]),
    .C(sel_q[1]),
    .Y(_0332_));
 sky130_fd_sc_hd__nor3b_1 _1145_ (.A(sel_q[2]),
    .B(sel_q[1]),
    .C_N(sel_q[0]),
    .Y(_0333_));
 sky130_fd_sc_hd__a22oi_1 _1146_ (.A1(osc[0]),
    .A2(_0332_),
    .B1(_0333_),
    .B2(osc[1]),
    .Y(_0334_));
 sky130_fd_sc_hd__nor3b_1 _1147_ (.A(sel_q[0]),
    .B(sel_q[1]),
    .C_N(sel_q[2]),
    .Y(_0335_));
 sky130_fd_sc_hd__and4b_1 _1148_ (.A_N(sel_q[2]),
    .B(sel_q[1]),
    .C(osc[3]),
    .D(sel_q[0]),
    .X(_0336_));
 sky130_fd_sc_hd__a21oi_1 _1149_ (.A1(osc[4]),
    .A2(_0335_),
    .B1(_0336_),
    .Y(_0337_));
 sky130_fd_sc_hd__nand3_1 _1150_ (.A(_0331_),
    .B(_0334_),
    .C(_0337_),
    .Y(osc_sel_clk));
 sky130_fd_sc_hd__nor3_1 _1151_ (.A(_0468_),
    .B(_0466_),
    .C(_0467_),
    .Y(_0338_));
 sky130_fd_sc_hd__nand3_1 _1152_ (.A(we),
    .B(_0648_),
    .C(_0338_),
    .Y(_0339_));
 sky130_fd_sc_hd__mux2_2 _1154_ (.A0(wdata[12]),
    .A1(\cal_r[0] [12]),
    .S(_0339_),
    .X(_0001_));
 sky130_fd_sc_hd__mux2_2 _1155_ (.A0(wdata[11]),
    .A1(\cal_r[0] [11]),
    .S(_0339_),
    .X(_0002_));
 sky130_fd_sc_hd__mux2_2 _1156_ (.A0(wdata[10]),
    .A1(\cal_r[0] [10]),
    .S(_0339_),
    .X(_0003_));
 sky130_fd_sc_hd__mux2_2 _1157_ (.A0(wdata[9]),
    .A1(\cal_r[0] [9]),
    .S(_0339_),
    .X(_0004_));
 sky130_fd_sc_hd__mux2_2 _1158_ (.A0(wdata[8]),
    .A1(\cal_r[0] [8]),
    .S(_0339_),
    .X(_0005_));
 sky130_fd_sc_hd__mux2_2 _1159_ (.A0(wdata[7]),
    .A1(\cal_r[0] [7]),
    .S(_0339_),
    .X(_0006_));
 sky130_fd_sc_hd__mux2_2 _1160_ (.A0(wdata[6]),
    .A1(\cal_r[0] [6]),
    .S(_0339_),
    .X(_0007_));
 sky130_fd_sc_hd__mux2_2 _1161_ (.A0(wdata[5]),
    .A1(\cal_r[0] [5]),
    .S(_0339_),
    .X(_0008_));
 sky130_fd_sc_hd__mux2_2 _1162_ (.A0(wdata[4]),
    .A1(\cal_r[0] [4]),
    .S(_0339_),
    .X(_0009_));
 sky130_fd_sc_hd__mux2_2 _1163_ (.A0(wdata[3]),
    .A1(\cal_r[0] [3]),
    .S(_0339_),
    .X(_0010_));
 sky130_fd_sc_hd__mux2_2 _1165_ (.A0(wdata[2]),
    .A1(\cal_r[0] [2]),
    .S(_0339_),
    .X(_0011_));
 sky130_fd_sc_hd__mux2_2 _1166_ (.A0(wdata[1]),
    .A1(\cal_r[0] [1]),
    .S(_0339_),
    .X(_0012_));
 sky130_fd_sc_hd__mux2_2 _1167_ (.A0(wdata[0]),
    .A1(\cal_r[0] [0]),
    .S(_0339_),
    .X(_0013_));
 sky130_fd_sc_hd__o21ai_0 _1168_ (.A1(tog_s2),
    .A2(tog_s3),
    .B1(busy_r),
    .Y(_0342_));
 sky130_fd_sc_hd__a21oi_1 _1169_ (.A1(tog_s2),
    .A2(tog_s3),
    .B1(_0342_),
    .Y(_0343_));
 sky130_fd_sc_hd__nand3_1 _1170_ (.A(sel_q[1]),
    .B(_0330_),
    .C(_0343_),
    .Y(_0344_));
 sky130_fd_sc_hd__mux2_2 _1172_ (.A0(cnt_o[22]),
    .A1(\count_r[2] [22]),
    .S(_0344_),
    .X(_0014_));
 sky130_fd_sc_hd__mux2_2 _1173_ (.A0(cnt_o[21]),
    .A1(\count_r[2] [21]),
    .S(_0344_),
    .X(_0015_));
 sky130_fd_sc_hd__mux2_2 _1174_ (.A0(cnt_o[20]),
    .A1(\count_r[2] [20]),
    .S(_0344_),
    .X(_0016_));
 sky130_fd_sc_hd__mux2_2 _1175_ (.A0(cnt_o[19]),
    .A1(\count_r[2] [19]),
    .S(_0344_),
    .X(_0017_));
 sky130_fd_sc_hd__mux2_2 _1176_ (.A0(cnt_o[18]),
    .A1(\count_r[2] [18]),
    .S(_0344_),
    .X(_0018_));
 sky130_fd_sc_hd__mux2_2 _1177_ (.A0(cnt_o[17]),
    .A1(\count_r[2] [17]),
    .S(_0344_),
    .X(_0019_));
 sky130_fd_sc_hd__mux2_2 _1178_ (.A0(cnt_o[16]),
    .A1(\count_r[2] [16]),
    .S(_0344_),
    .X(_0020_));
 sky130_fd_sc_hd__mux2_2 _1179_ (.A0(cnt_o[15]),
    .A1(\count_r[2] [15]),
    .S(_0344_),
    .X(_0021_));
 sky130_fd_sc_hd__mux2_2 _1180_ (.A0(cnt_o[14]),
    .A1(\count_r[2] [14]),
    .S(_0344_),
    .X(_0022_));
 sky130_fd_sc_hd__mux2_2 _1181_ (.A0(cnt_o[13]),
    .A1(\count_r[2] [13]),
    .S(_0344_),
    .X(_0023_));
 sky130_fd_sc_hd__mux2_2 _1183_ (.A0(cnt_o[12]),
    .A1(\count_r[2] [12]),
    .S(_0344_),
    .X(_0024_));
 sky130_fd_sc_hd__mux2_2 _1184_ (.A0(cnt_o[11]),
    .A1(\count_r[2] [11]),
    .S(_0344_),
    .X(_0025_));
 sky130_fd_sc_hd__mux2_2 _1185_ (.A0(cnt_o[10]),
    .A1(\count_r[2] [10]),
    .S(_0344_),
    .X(_0026_));
 sky130_fd_sc_hd__mux2_2 _1186_ (.A0(cnt_o[9]),
    .A1(\count_r[2] [9]),
    .S(_0344_),
    .X(_0027_));
 sky130_fd_sc_hd__mux2_2 _1187_ (.A0(cnt_o[8]),
    .A1(\count_r[2] [8]),
    .S(_0344_),
    .X(_0028_));
 sky130_fd_sc_hd__mux2_2 _1188_ (.A0(cnt_o[7]),
    .A1(\count_r[2] [7]),
    .S(_0344_),
    .X(_0029_));
 sky130_fd_sc_hd__mux2_2 _1189_ (.A0(cnt_o[6]),
    .A1(\count_r[2] [6]),
    .S(_0344_),
    .X(_0030_));
 sky130_fd_sc_hd__mux2_2 _1190_ (.A0(cnt_o[5]),
    .A1(\count_r[2] [5]),
    .S(_0344_),
    .X(_0031_));
 sky130_fd_sc_hd__mux2_2 _1191_ (.A0(cnt_o[4]),
    .A1(\count_r[2] [4]),
    .S(_0344_),
    .X(_0032_));
 sky130_fd_sc_hd__mux2_2 _1192_ (.A0(cnt_o[3]),
    .A1(\count_r[2] [3]),
    .S(_0344_),
    .X(_0033_));
 sky130_fd_sc_hd__mux2_2 _1193_ (.A0(cnt_o[2]),
    .A1(\count_r[2] [2]),
    .S(_0344_),
    .X(_0034_));
 sky130_fd_sc_hd__mux2_2 _1194_ (.A0(cnt_o[1]),
    .A1(\count_r[2] [1]),
    .S(_0344_),
    .X(_0035_));
 sky130_fd_sc_hd__mux2_2 _1195_ (.A0(cnt_o[0]),
    .A1(\count_r[2] [0]),
    .S(_0344_),
    .X(_0036_));
 sky130_fd_sc_hd__nor2_1 _1196_ (.A(sel_q[1]),
    .B(net13),
    .Y(_0347_));
 sky130_fd_sc_hd__nand4bb_1 _1197_ (.A_N(busy_r),
    .B_N(_0313_),
    .C(_0314_),
    .D(wdata[0]),
    .Y(_0348_));
 sky130_fd_sc_hd__nor2_1 _1199_ (.A(wdata[2]),
    .B(_0348_),
    .Y(_0350_));
 sky130_fd_sc_hd__nor2_1 _1200_ (.A(_0347_),
    .B(_0350_),
    .Y(_0037_));
 sky130_fd_sc_hd__nor2_1 _1201_ (.A(sel_q[0]),
    .B(net13),
    .Y(_0351_));
 sky130_fd_sc_hd__nor2_1 _1202_ (.A(wdata[1]),
    .B(_0348_),
    .Y(_0352_));
 sky130_fd_sc_hd__nor2_1 _1203_ (.A(_0351_),
    .B(_0352_),
    .Y(_0038_));
 sky130_fd_sc_hd__nand4b_1 _1204_ (.A_N(sel_q[2]),
    .B(sel_q[1]),
    .C(_0343_),
    .D(sel_q[0]),
    .Y(_0353_));
 sky130_fd_sc_hd__mux2_2 _1206_ (.A0(cnt_o[22]),
    .A1(\count_r[3] [22]),
    .S(net12),
    .X(_0039_));
 sky130_fd_sc_hd__mux2_2 _1207_ (.A0(cnt_o[21]),
    .A1(\count_r[3] [21]),
    .S(net12),
    .X(_0040_));
 sky130_fd_sc_hd__mux2_2 _1208_ (.A0(cnt_o[20]),
    .A1(\count_r[3] [20]),
    .S(net12),
    .X(_0041_));
 sky130_fd_sc_hd__mux2_2 _1209_ (.A0(cnt_o[19]),
    .A1(\count_r[3] [19]),
    .S(net12),
    .X(_0042_));
 sky130_fd_sc_hd__mux2_2 _1210_ (.A0(cnt_o[18]),
    .A1(\count_r[3] [18]),
    .S(net12),
    .X(_0043_));
 sky130_fd_sc_hd__mux2_2 _1211_ (.A0(cnt_o[17]),
    .A1(\count_r[3] [17]),
    .S(net12),
    .X(_0044_));
 sky130_fd_sc_hd__mux2_2 _1212_ (.A0(cnt_o[16]),
    .A1(\count_r[3] [16]),
    .S(net12),
    .X(_0045_));
 sky130_fd_sc_hd__mux2_2 _1213_ (.A0(cnt_o[15]),
    .A1(\count_r[3] [15]),
    .S(net12),
    .X(_0046_));
 sky130_fd_sc_hd__mux2_2 _1214_ (.A0(cnt_o[14]),
    .A1(\count_r[3] [14]),
    .S(net12),
    .X(_0047_));
 sky130_fd_sc_hd__mux2_2 _1215_ (.A0(cnt_o[13]),
    .A1(\count_r[3] [13]),
    .S(net12),
    .X(_0048_));
 sky130_fd_sc_hd__mux2_2 _1217_ (.A0(cnt_o[12]),
    .A1(\count_r[3] [12]),
    .S(net12),
    .X(_0049_));
 sky130_fd_sc_hd__mux2_2 _1218_ (.A0(cnt_o[11]),
    .A1(\count_r[3] [11]),
    .S(net12),
    .X(_0050_));
 sky130_fd_sc_hd__mux2_2 _1219_ (.A0(cnt_o[10]),
    .A1(\count_r[3] [10]),
    .S(net12),
    .X(_0051_));
 sky130_fd_sc_hd__mux2_2 _1220_ (.A0(cnt_o[9]),
    .A1(\count_r[3] [9]),
    .S(net12),
    .X(_0052_));
 sky130_fd_sc_hd__mux2_2 _1221_ (.A0(cnt_o[8]),
    .A1(\count_r[3] [8]),
    .S(net12),
    .X(_0053_));
 sky130_fd_sc_hd__mux2_2 _1222_ (.A0(cnt_o[7]),
    .A1(\count_r[3] [7]),
    .S(net12),
    .X(_0054_));
 sky130_fd_sc_hd__mux2_2 _1223_ (.A0(cnt_o[6]),
    .A1(\count_r[3] [6]),
    .S(net12),
    .X(_0055_));
 sky130_fd_sc_hd__mux2_2 _1224_ (.A0(cnt_o[5]),
    .A1(\count_r[3] [5]),
    .S(net12),
    .X(_0056_));
 sky130_fd_sc_hd__mux2_2 _1225_ (.A0(cnt_o[4]),
    .A1(\count_r[3] [4]),
    .S(net12),
    .X(_0057_));
 sky130_fd_sc_hd__mux2_2 _1226_ (.A0(cnt_o[3]),
    .A1(\count_r[3] [3]),
    .S(net12),
    .X(_0058_));
 sky130_fd_sc_hd__mux2_2 _1227_ (.A0(cnt_o[2]),
    .A1(\count_r[3] [2]),
    .S(net12),
    .X(_0059_));
 sky130_fd_sc_hd__mux2_2 _1228_ (.A0(cnt_o[1]),
    .A1(\count_r[3] [1]),
    .S(net12),
    .X(_0060_));
 sky130_fd_sc_hd__mux2_2 _1229_ (.A0(cnt_o[0]),
    .A1(\count_r[3] [0]),
    .S(net12),
    .X(_0061_));
 sky130_fd_sc_hd__nand2_1 _1230_ (.A(_0333_),
    .B(_0343_),
    .Y(_0356_));
 sky130_fd_sc_hd__mux2_2 _1232_ (.A0(cnt_o[22]),
    .A1(\count_r[1] [22]),
    .S(_0356_),
    .X(_0062_));
 sky130_fd_sc_hd__mux2_2 _1233_ (.A0(cnt_o[21]),
    .A1(\count_r[1] [21]),
    .S(_0356_),
    .X(_0063_));
 sky130_fd_sc_hd__mux2_2 _1234_ (.A0(cnt_o[20]),
    .A1(\count_r[1] [20]),
    .S(_0356_),
    .X(_0064_));
 sky130_fd_sc_hd__mux2_2 _1235_ (.A0(cnt_o[19]),
    .A1(\count_r[1] [19]),
    .S(_0356_),
    .X(_0065_));
 sky130_fd_sc_hd__mux2_2 _1236_ (.A0(cnt_o[18]),
    .A1(\count_r[1] [18]),
    .S(_0356_),
    .X(_0066_));
 sky130_fd_sc_hd__mux2_2 _1237_ (.A0(cnt_o[17]),
    .A1(\count_r[1] [17]),
    .S(_0356_),
    .X(_0067_));
 sky130_fd_sc_hd__mux2_2 _1238_ (.A0(cnt_o[16]),
    .A1(\count_r[1] [16]),
    .S(_0356_),
    .X(_0068_));
 sky130_fd_sc_hd__mux2_2 _1239_ (.A0(cnt_o[15]),
    .A1(\count_r[1] [15]),
    .S(_0356_),
    .X(_0069_));
 sky130_fd_sc_hd__mux2_2 _1240_ (.A0(cnt_o[14]),
    .A1(\count_r[1] [14]),
    .S(_0356_),
    .X(_0070_));
 sky130_fd_sc_hd__mux2_2 _1241_ (.A0(cnt_o[13]),
    .A1(\count_r[1] [13]),
    .S(_0356_),
    .X(_0071_));
 sky130_fd_sc_hd__mux2_2 _1243_ (.A0(cnt_o[12]),
    .A1(\count_r[1] [12]),
    .S(_0356_),
    .X(_0072_));
 sky130_fd_sc_hd__mux2_2 _1244_ (.A0(cnt_o[11]),
    .A1(\count_r[1] [11]),
    .S(_0356_),
    .X(_0073_));
 sky130_fd_sc_hd__mux2_2 _1245_ (.A0(cnt_o[10]),
    .A1(\count_r[1] [10]),
    .S(_0356_),
    .X(_0074_));
 sky130_fd_sc_hd__mux2_2 _1246_ (.A0(cnt_o[9]),
    .A1(\count_r[1] [9]),
    .S(_0356_),
    .X(_0075_));
 sky130_fd_sc_hd__mux2_2 _1247_ (.A0(cnt_o[8]),
    .A1(\count_r[1] [8]),
    .S(_0356_),
    .X(_0076_));
 sky130_fd_sc_hd__mux2_2 _1248_ (.A0(cnt_o[7]),
    .A1(\count_r[1] [7]),
    .S(_0356_),
    .X(_0077_));
 sky130_fd_sc_hd__mux2_2 _1249_ (.A0(cnt_o[6]),
    .A1(\count_r[1] [6]),
    .S(_0356_),
    .X(_0078_));
 sky130_fd_sc_hd__mux2_2 _1250_ (.A0(cnt_o[5]),
    .A1(\count_r[1] [5]),
    .S(_0356_),
    .X(_0079_));
 sky130_fd_sc_hd__mux2_2 _1251_ (.A0(cnt_o[4]),
    .A1(\count_r[1] [4]),
    .S(_0356_),
    .X(_0080_));
 sky130_fd_sc_hd__mux2_2 _1252_ (.A0(cnt_o[3]),
    .A1(\count_r[1] [3]),
    .S(_0356_),
    .X(_0081_));
 sky130_fd_sc_hd__mux2_2 _1253_ (.A0(cnt_o[2]),
    .A1(\count_r[1] [2]),
    .S(_0356_),
    .X(_0082_));
 sky130_fd_sc_hd__mux2_2 _1254_ (.A0(cnt_o[1]),
    .A1(\count_r[1] [1]),
    .S(_0356_),
    .X(_0083_));
 sky130_fd_sc_hd__mux2_2 _1255_ (.A0(cnt_o[0]),
    .A1(\count_r[1] [0]),
    .S(_0356_),
    .X(_0084_));
 sky130_fd_sc_hd__mux2_2 _1256_ (.A0(wdata[2]),
    .A1(ctrl_sel[1]),
    .S(_0313_),
    .X(_0085_));
 sky130_fd_sc_hd__mux2_2 _1257_ (.A0(wdata[1]),
    .A1(ctrl_sel[0]),
    .S(_0313_),
    .X(_0086_));
 sky130_fd_sc_hd__nand3_1 _1258_ (.A(we),
    .B(_0648_),
    .C(net19),
    .Y(_0359_));
 sky130_fd_sc_hd__mux2_2 _1260_ (.A0(wdata[20]),
    .A1(\cal_r[2] [20]),
    .S(_0359_),
    .X(_0087_));
 sky130_fd_sc_hd__mux2_2 _1261_ (.A0(wdata[19]),
    .A1(\cal_r[2] [19]),
    .S(net11),
    .X(_0088_));
 sky130_fd_sc_hd__mux2_2 _1262_ (.A0(wdata[18]),
    .A1(\cal_r[2] [18]),
    .S(net11),
    .X(_0089_));
 sky130_fd_sc_hd__mux2_2 _1263_ (.A0(wdata[17]),
    .A1(\cal_r[2] [17]),
    .S(net11),
    .X(_0090_));
 sky130_fd_sc_hd__mux2_2 _1264_ (.A0(wdata[16]),
    .A1(\cal_r[2] [16]),
    .S(_0359_),
    .X(_0091_));
 sky130_fd_sc_hd__mux2_2 _1265_ (.A0(wdata[15]),
    .A1(\cal_r[2] [15]),
    .S(net11),
    .X(_0092_));
 sky130_fd_sc_hd__mux2_2 _1266_ (.A0(wdata[14]),
    .A1(\cal_r[2] [14]),
    .S(net11),
    .X(_0093_));
 sky130_fd_sc_hd__mux2_2 _1267_ (.A0(wdata[13]),
    .A1(\cal_r[2] [13]),
    .S(net11),
    .X(_0094_));
 sky130_fd_sc_hd__mux2_2 _1268_ (.A0(wdata[12]),
    .A1(\cal_r[2] [12]),
    .S(net11),
    .X(_0095_));
 sky130_fd_sc_hd__mux2_2 _1269_ (.A0(wdata[11]),
    .A1(\cal_r[2] [11]),
    .S(net11),
    .X(_0096_));
 sky130_fd_sc_hd__mux2_2 _1271_ (.A0(wdata[10]),
    .A1(\cal_r[2] [10]),
    .S(net11),
    .X(_0097_));
 sky130_fd_sc_hd__mux2_2 _1272_ (.A0(wdata[9]),
    .A1(\cal_r[2] [9]),
    .S(_0359_),
    .X(_0098_));
 sky130_fd_sc_hd__mux2_2 _1273_ (.A0(wdata[8]),
    .A1(\cal_r[2] [8]),
    .S(net11),
    .X(_0099_));
 sky130_fd_sc_hd__mux2_2 _1274_ (.A0(wdata[7]),
    .A1(\cal_r[2] [7]),
    .S(net11),
    .X(_0100_));
 sky130_fd_sc_hd__mux2_2 _1275_ (.A0(wdata[6]),
    .A1(\cal_r[2] [6]),
    .S(net11),
    .X(_0101_));
 sky130_fd_sc_hd__mux2_2 _1276_ (.A0(wdata[5]),
    .A1(\cal_r[2] [5]),
    .S(_0359_),
    .X(_0102_));
 sky130_fd_sc_hd__mux2_2 _1277_ (.A0(wdata[4]),
    .A1(\cal_r[2] [4]),
    .S(net11),
    .X(_0103_));
 sky130_fd_sc_hd__mux2_2 _1278_ (.A0(wdata[3]),
    .A1(\cal_r[2] [3]),
    .S(net11),
    .X(_0104_));
 sky130_fd_sc_hd__mux2_2 _1279_ (.A0(wdata[2]),
    .A1(\cal_r[2] [2]),
    .S(net11),
    .X(_0105_));
 sky130_fd_sc_hd__mux2_2 _1280_ (.A0(wdata[1]),
    .A1(\cal_r[2] [1]),
    .S(net11),
    .X(_0106_));
 sky130_fd_sc_hd__mux2_2 _1281_ (.A0(wdata[0]),
    .A1(\cal_r[2] [0]),
    .S(net11),
    .X(_0107_));
 sky130_fd_sc_hd__mux2_2 _1282_ (.A0(wdata[22]),
    .A1(\cal_r[2] [22]),
    .S(net11),
    .X(_0108_));
 sky130_fd_sc_hd__mux2_2 _1283_ (.A0(wdata[21]),
    .A1(\cal_r[2] [21]),
    .S(_0359_),
    .X(_0109_));
 sky130_fd_sc_hd__nand2_1 _1284_ (.A(_0335_),
    .B(_0343_),
    .Y(_0362_));
 sky130_fd_sc_hd__mux2_2 _1286_ (.A0(cnt_o[22]),
    .A1(\count_r[4] [22]),
    .S(_0362_),
    .X(_0110_));
 sky130_fd_sc_hd__mux2_2 _1287_ (.A0(cnt_o[21]),
    .A1(\count_r[4] [21]),
    .S(_0362_),
    .X(_0111_));
 sky130_fd_sc_hd__mux2_2 _1288_ (.A0(cnt_o[20]),
    .A1(\count_r[4] [20]),
    .S(_0362_),
    .X(_0112_));
 sky130_fd_sc_hd__mux2_2 _1289_ (.A0(cnt_o[19]),
    .A1(\count_r[4] [19]),
    .S(_0362_),
    .X(_0113_));
 sky130_fd_sc_hd__mux2_2 _1290_ (.A0(cnt_o[18]),
    .A1(\count_r[4] [18]),
    .S(_0362_),
    .X(_0114_));
 sky130_fd_sc_hd__mux2_2 _1291_ (.A0(cnt_o[17]),
    .A1(\count_r[4] [17]),
    .S(_0362_),
    .X(_0115_));
 sky130_fd_sc_hd__mux2_2 _1292_ (.A0(cnt_o[16]),
    .A1(\count_r[4] [16]),
    .S(_0362_),
    .X(_0116_));
 sky130_fd_sc_hd__mux2_2 _1293_ (.A0(cnt_o[15]),
    .A1(\count_r[4] [15]),
    .S(_0362_),
    .X(_0117_));
 sky130_fd_sc_hd__mux2_2 _1294_ (.A0(cnt_o[14]),
    .A1(\count_r[4] [14]),
    .S(_0362_),
    .X(_0118_));
 sky130_fd_sc_hd__mux2_2 _1295_ (.A0(cnt_o[13]),
    .A1(\count_r[4] [13]),
    .S(_0362_),
    .X(_0119_));
 sky130_fd_sc_hd__mux2_2 _1297_ (.A0(cnt_o[12]),
    .A1(\count_r[4] [12]),
    .S(_0362_),
    .X(_0120_));
 sky130_fd_sc_hd__mux2_2 _1298_ (.A0(cnt_o[11]),
    .A1(\count_r[4] [11]),
    .S(_0362_),
    .X(_0121_));
 sky130_fd_sc_hd__mux2_2 _1299_ (.A0(cnt_o[10]),
    .A1(\count_r[4] [10]),
    .S(_0362_),
    .X(_0122_));
 sky130_fd_sc_hd__mux2_2 _1300_ (.A0(cnt_o[9]),
    .A1(\count_r[4] [9]),
    .S(_0362_),
    .X(_0123_));
 sky130_fd_sc_hd__mux2_2 _1301_ (.A0(cnt_o[8]),
    .A1(\count_r[4] [8]),
    .S(_0362_),
    .X(_0124_));
 sky130_fd_sc_hd__mux2_2 _1302_ (.A0(cnt_o[7]),
    .A1(\count_r[4] [7]),
    .S(_0362_),
    .X(_0125_));
 sky130_fd_sc_hd__mux2_2 _1303_ (.A0(cnt_o[6]),
    .A1(\count_r[4] [6]),
    .S(_0362_),
    .X(_0126_));
 sky130_fd_sc_hd__mux2_2 _1304_ (.A0(cnt_o[5]),
    .A1(\count_r[4] [5]),
    .S(_0362_),
    .X(_0127_));
 sky130_fd_sc_hd__mux2_2 _1305_ (.A0(cnt_o[4]),
    .A1(\count_r[4] [4]),
    .S(_0362_),
    .X(_0128_));
 sky130_fd_sc_hd__mux2_2 _1306_ (.A0(cnt_o[3]),
    .A1(\count_r[4] [3]),
    .S(_0362_),
    .X(_0129_));
 sky130_fd_sc_hd__mux2_2 _1307_ (.A0(cnt_o[2]),
    .A1(\count_r[4] [2]),
    .S(_0362_),
    .X(_0130_));
 sky130_fd_sc_hd__mux2_2 _1308_ (.A0(cnt_o[1]),
    .A1(\count_r[4] [1]),
    .S(_0362_),
    .X(_0131_));
 sky130_fd_sc_hd__mux2_2 _1309_ (.A0(cnt_o[0]),
    .A1(\count_r[4] [0]),
    .S(_0362_),
    .X(_0132_));
 sky130_fd_sc_hd__nand3_1 _1310_ (.A(we),
    .B(net15),
    .C(_0648_),
    .Y(_0365_));
 sky130_fd_sc_hd__mux2_2 _1312_ (.A0(wdata[22]),
    .A1(\cal_r[3] [22]),
    .S(_0365_),
    .X(_0133_));
 sky130_fd_sc_hd__mux2_2 _1313_ (.A0(wdata[21]),
    .A1(\cal_r[3] [21]),
    .S(_0365_),
    .X(_0134_));
 sky130_fd_sc_hd__mux2_2 _1314_ (.A0(wdata[20]),
    .A1(\cal_r[3] [20]),
    .S(_0365_),
    .X(_0135_));
 sky130_fd_sc_hd__mux2_2 _1315_ (.A0(wdata[19]),
    .A1(\cal_r[3] [19]),
    .S(_0365_),
    .X(_0136_));
 sky130_fd_sc_hd__mux2_2 _1316_ (.A0(wdata[18]),
    .A1(\cal_r[3] [18]),
    .S(_0365_),
    .X(_0137_));
 sky130_fd_sc_hd__mux2_2 _1317_ (.A0(wdata[17]),
    .A1(\cal_r[3] [17]),
    .S(_0365_),
    .X(_0138_));
 sky130_fd_sc_hd__mux2_2 _1318_ (.A0(wdata[16]),
    .A1(\cal_r[3] [16]),
    .S(_0365_),
    .X(_0139_));
 sky130_fd_sc_hd__mux2_2 _1319_ (.A0(wdata[15]),
    .A1(\cal_r[3] [15]),
    .S(_0365_),
    .X(_0140_));
 sky130_fd_sc_hd__mux2_2 _1320_ (.A0(wdata[14]),
    .A1(\cal_r[3] [14]),
    .S(_0365_),
    .X(_0141_));
 sky130_fd_sc_hd__mux2_2 _1321_ (.A0(wdata[13]),
    .A1(\cal_r[3] [13]),
    .S(_0365_),
    .X(_0142_));
 sky130_fd_sc_hd__mux2_2 _1323_ (.A0(wdata[12]),
    .A1(\cal_r[3] [12]),
    .S(_0365_),
    .X(_0143_));
 sky130_fd_sc_hd__mux2_2 _1324_ (.A0(wdata[11]),
    .A1(\cal_r[3] [11]),
    .S(_0365_),
    .X(_0144_));
 sky130_fd_sc_hd__mux2_2 _1325_ (.A0(wdata[10]),
    .A1(\cal_r[3] [10]),
    .S(_0365_),
    .X(_0145_));
 sky130_fd_sc_hd__mux2_2 _1326_ (.A0(wdata[9]),
    .A1(\cal_r[3] [9]),
    .S(_0365_),
    .X(_0146_));
 sky130_fd_sc_hd__mux2_2 _1327_ (.A0(wdata[8]),
    .A1(\cal_r[3] [8]),
    .S(_0365_),
    .X(_0147_));
 sky130_fd_sc_hd__mux2_2 _1328_ (.A0(wdata[7]),
    .A1(\cal_r[3] [7]),
    .S(_0365_),
    .X(_0148_));
 sky130_fd_sc_hd__mux2_2 _1329_ (.A0(wdata[6]),
    .A1(\cal_r[3] [6]),
    .S(_0365_),
    .X(_0149_));
 sky130_fd_sc_hd__mux2_2 _1330_ (.A0(wdata[5]),
    .A1(\cal_r[3] [5]),
    .S(_0365_),
    .X(_0150_));
 sky130_fd_sc_hd__mux2_2 _1331_ (.A0(wdata[4]),
    .A1(\cal_r[3] [4]),
    .S(_0365_),
    .X(_0151_));
 sky130_fd_sc_hd__mux2_2 _1332_ (.A0(wdata[3]),
    .A1(\cal_r[3] [3]),
    .S(_0365_),
    .X(_0152_));
 sky130_fd_sc_hd__mux2_2 _1333_ (.A0(wdata[2]),
    .A1(\cal_r[3] [2]),
    .S(_0365_),
    .X(_0153_));
 sky130_fd_sc_hd__mux2_2 _1334_ (.A0(wdata[1]),
    .A1(\cal_r[3] [1]),
    .S(_0365_),
    .X(_0154_));
 sky130_fd_sc_hd__mux2_2 _1335_ (.A0(wdata[0]),
    .A1(\cal_r[3] [0]),
    .S(_0365_),
    .X(_0155_));
 sky130_fd_sc_hd__nand4_1 _1336_ (.A(gate_cnt[10]),
    .B(gate_cnt[11]),
    .C(gate_cnt[12]),
    .D(gate_cnt[13]),
    .Y(_0368_));
 sky130_fd_sc_hd__nand2_1 _1337_ (.A(gate_cnt[9]),
    .B(gate_cnt[14]),
    .Y(_0369_));
 sky130_fd_sc_hd__nor2_1 _1338_ (.A(_0368_),
    .B(_0369_),
    .Y(_0370_));
 sky130_fd_sc_hd__nand4_1 _1339_ (.A(gate_cnt[4]),
    .B(gate_cnt[2]),
    .C(gate_cnt[1]),
    .D(gate_cnt[0]),
    .Y(_0371_));
 sky130_fd_sc_hd__nand2_1 _1340_ (.A(gate_cnt[7]),
    .B(gate_cnt[8]),
    .Y(_0372_));
 sky130_fd_sc_hd__nand2_1 _1341_ (.A(gate_cnt[26]),
    .B(gate_cnt[27]),
    .Y(_0373_));
 sky130_fd_sc_hd__nor3_1 _1342_ (.A(_0371_),
    .B(_0372_),
    .C(_0373_),
    .Y(_0374_));
 sky130_fd_sc_hd__nand4_1 _1343_ (.A(gate_cnt[16]),
    .B(gate_cnt[17]),
    .C(gate_cnt[22]),
    .D(gate_cnt[23]),
    .Y(_0375_));
 sky130_fd_sc_hd__nand4_1 _1344_ (.A(gate_cnt[3]),
    .B(gate_cnt[5]),
    .C(gate_cnt[6]),
    .D(gate_cnt[15]),
    .Y(_0376_));
 sky130_fd_sc_hd__nand4_1 _1345_ (.A(gate_cnt[18]),
    .B(gate_cnt[19]),
    .C(gate_cnt[20]),
    .D(gate_cnt[21]),
    .Y(_0377_));
 sky130_fd_sc_hd__nand3_1 _1346_ (.A(gate_cnt[24]),
    .B(gate_cnt[25]),
    .C(gate_en),
    .Y(_0378_));
 sky130_fd_sc_hd__nor4_1 _1347_ (.A(_0375_),
    .B(_0376_),
    .C(_0377_),
    .D(_0378_),
    .Y(_0379_));
 sky130_fd_sc_hd__nand4_1 _1348_ (.A(gate_cnt[28]),
    .B(_0370_),
    .C(_0374_),
    .D(_0379_),
    .Y(_0380_));
 sky130_fd_sc_hd__nor2_1 _1349_ (.A(_0701_),
    .B(_0380_),
    .Y(_0381_));
 sky130_fd_sc_hd__o21ai_0 _1351_ (.A1(gate_cnt[30]),
    .A2(_0381_),
    .B1(_0348_),
    .Y(_0383_));
 sky130_fd_sc_hd__a21oi_1 _1352_ (.A1(gate_cnt[30]),
    .A2(_0381_),
    .B1(_0383_),
    .Y(_0156_));
 sky130_fd_sc_hd__nand2_1 _1353_ (.A(_0701_),
    .B(_0380_),
    .Y(_0384_));
 sky130_fd_sc_hd__nor3b_1 _1354_ (.A(net13),
    .B(_0381_),
    .C_N(_0384_),
    .Y(_0157_));
 sky130_fd_sc_hd__a31oi_1 _1355_ (.A1(_0370_),
    .A2(_0374_),
    .A3(_0379_),
    .B1(gate_cnt[28]),
    .Y(_0385_));
 sky130_fd_sc_hd__nand2_1 _1356_ (.A(_0348_),
    .B(_0380_),
    .Y(_0386_));
 sky130_fd_sc_hd__nor2_1 _1357_ (.A(_0385_),
    .B(_0386_),
    .Y(_0158_));
 sky130_fd_sc_hd__inv_1 _1358_ (.A(_0373_),
    .Y(_0387_));
 sky130_fd_sc_hd__inv_1 _1359_ (.A(_0377_),
    .Y(_0388_));
 sky130_fd_sc_hd__and2_2 _1360_ (.A(gate_cnt[7]),
    .B(gate_cnt[8]),
    .X(_0389_));
 sky130_fd_sc_hd__and4_4 _1361_ (.A(gate_cnt[2]),
    .B(gate_cnt[1]),
    .C(gate_cnt[0]),
    .D(gate_en),
    .X(_0390_));
 sky130_fd_sc_hd__and4_4 _1362_ (.A(gate_cnt[4]),
    .B(gate_cnt[3]),
    .C(gate_cnt[5]),
    .D(_0390_),
    .X(_0391_));
 sky130_fd_sc_hd__and4_4 _1363_ (.A(gate_cnt[6]),
    .B(_0370_),
    .C(_0389_),
    .D(_0391_),
    .X(_0392_));
 sky130_fd_sc_hd__and4_4 _1364_ (.A(gate_cnt[15]),
    .B(gate_cnt[16]),
    .C(gate_cnt[17]),
    .D(_0392_),
    .X(_0393_));
 sky130_fd_sc_hd__and4_1 _1365_ (.A(gate_cnt[22]),
    .B(gate_cnt[23]),
    .C(_0388_),
    .D(_0393_),
    .X(_0394_));
 sky130_fd_sc_hd__and3_2 _1367_ (.A(gate_cnt[24]),
    .B(gate_cnt[25]),
    .C(_0394_),
    .X(_0396_));
 sky130_fd_sc_hd__a41oi_2 _1368_ (.A1(gate_cnt[24]),
    .A2(gate_cnt[25]),
    .A3(gate_cnt[26]),
    .A4(_0394_),
    .B1(gate_cnt[27]),
    .Y(_0397_));
 sky130_fd_sc_hd__a211oi_2 _1370_ (.A1(_0387_),
    .A2(_0396_),
    .B1(_0397_),
    .C1(net13),
    .Y(_0159_));
 sky130_fd_sc_hd__a31oi_1 _1371_ (.A1(gate_cnt[24]),
    .A2(gate_cnt[25]),
    .A3(_0394_),
    .B1(gate_cnt[26]),
    .Y(_0399_));
 sky130_fd_sc_hd__a211oi_1 _1372_ (.A1(gate_cnt[26]),
    .A2(_0396_),
    .B1(_0399_),
    .C1(net13),
    .Y(_0160_));
 sky130_fd_sc_hd__a21oi_1 _1374_ (.A1(gate_cnt[24]),
    .A2(_0394_),
    .B1(gate_cnt[25]),
    .Y(_0401_));
 sky130_fd_sc_hd__nor3_1 _1375_ (.A(net13),
    .B(_0396_),
    .C(_0401_),
    .Y(_0161_));
 sky130_fd_sc_hd__a21oi_1 _1376_ (.A1(gate_cnt[24]),
    .A2(_0394_),
    .B1(net13),
    .Y(_0402_));
 sky130_fd_sc_hd__o21a_1 _1377_ (.A1(gate_cnt[24]),
    .A2(_0394_),
    .B1(_0402_),
    .X(_0162_));
 sky130_fd_sc_hd__and2_2 _1378_ (.A(_0388_),
    .B(_0393_),
    .X(_0403_));
 sky130_fd_sc_hd__a21oi_1 _1379_ (.A1(gate_cnt[22]),
    .A2(_0403_),
    .B1(gate_cnt[23]),
    .Y(_0404_));
 sky130_fd_sc_hd__nor3_1 _1380_ (.A(net13),
    .B(_0394_),
    .C(_0404_),
    .Y(_0163_));
 sky130_fd_sc_hd__a21oi_1 _1381_ (.A1(gate_cnt[22]),
    .A2(_0403_),
    .B1(net13),
    .Y(_0405_));
 sky130_fd_sc_hd__o21a_1 _1382_ (.A1(gate_cnt[22]),
    .A2(_0403_),
    .B1(_0405_),
    .X(_0164_));
 sky130_fd_sc_hd__and2_1 _1383_ (.A(gate_cnt[18]),
    .B(_0393_),
    .X(_0406_));
 sky130_fd_sc_hd__a31oi_1 _1384_ (.A1(gate_cnt[19]),
    .A2(gate_cnt[20]),
    .A3(_0406_),
    .B1(gate_cnt[21]),
    .Y(_0407_));
 sky130_fd_sc_hd__nor3_1 _1385_ (.A(net13),
    .B(_0403_),
    .C(_0407_),
    .Y(_0165_));
 sky130_fd_sc_hd__and3_1 _1386_ (.A(gate_cnt[19]),
    .B(gate_cnt[20]),
    .C(_0406_),
    .X(_0408_));
 sky130_fd_sc_hd__a21oi_1 _1387_ (.A1(gate_cnt[19]),
    .A2(_0406_),
    .B1(gate_cnt[20]),
    .Y(_0409_));
 sky130_fd_sc_hd__nor3_1 _1388_ (.A(net13),
    .B(_0408_),
    .C(_0409_),
    .Y(_0166_));
 sky130_fd_sc_hd__nor2_1 _1389_ (.A(gate_cnt[19]),
    .B(_0406_),
    .Y(_0410_));
 sky130_fd_sc_hd__a211oi_1 _1390_ (.A1(gate_cnt[19]),
    .A2(_0406_),
    .B1(_0410_),
    .C1(net13),
    .Y(_0167_));
 sky130_fd_sc_hd__nor2_1 _1391_ (.A(gate_cnt[18]),
    .B(_0393_),
    .Y(_0411_));
 sky130_fd_sc_hd__nor3_1 _1392_ (.A(net13),
    .B(_0406_),
    .C(_0411_),
    .Y(_0168_));
 sky130_fd_sc_hd__and3_2 _1393_ (.A(gate_cnt[15]),
    .B(gate_cnt[16]),
    .C(_0392_),
    .X(_0412_));
 sky130_fd_sc_hd__nor2_1 _1394_ (.A(gate_cnt[17]),
    .B(_0412_),
    .Y(_0413_));
 sky130_fd_sc_hd__nor3_1 _1395_ (.A(net13),
    .B(_0393_),
    .C(_0413_),
    .Y(_0169_));
 sky130_fd_sc_hd__a21oi_1 _1396_ (.A1(gate_cnt[15]),
    .A2(_0392_),
    .B1(gate_cnt[16]),
    .Y(_0414_));
 sky130_fd_sc_hd__nor3_1 _1397_ (.A(net13),
    .B(_0412_),
    .C(_0414_),
    .Y(_0170_));
 sky130_fd_sc_hd__and3_2 _1398_ (.A(gate_cnt[6]),
    .B(_0389_),
    .C(_0391_),
    .X(_0415_));
 sky130_fd_sc_hd__and2_1 _1399_ (.A(gate_cnt[9]),
    .B(_0415_),
    .X(_0416_));
 sky130_fd_sc_hd__nor2b_1 _1400_ (.A(_0368_),
    .B_N(_0416_),
    .Y(_0417_));
 sky130_fd_sc_hd__and2_1 _1401_ (.A(gate_cnt[14]),
    .B(_0417_),
    .X(_0418_));
 sky130_fd_sc_hd__o21ai_0 _1402_ (.A1(gate_cnt[15]),
    .A2(_0392_),
    .B1(_0348_),
    .Y(_0419_));
 sky130_fd_sc_hd__a21oi_1 _1403_ (.A1(gate_cnt[15]),
    .A2(_0418_),
    .B1(_0419_),
    .Y(_0171_));
 sky130_fd_sc_hd__o21ai_0 _1404_ (.A1(gate_cnt[14]),
    .A2(_0417_),
    .B1(_0348_),
    .Y(_0420_));
 sky130_fd_sc_hd__nor2_1 _1405_ (.A(_0418_),
    .B(_0420_),
    .Y(_0172_));
 sky130_fd_sc_hd__and3_1 _1406_ (.A(gate_cnt[9]),
    .B(gate_cnt[10]),
    .C(_0415_),
    .X(_0421_));
 sky130_fd_sc_hd__and2_1 _1407_ (.A(gate_cnt[11]),
    .B(_0421_),
    .X(_0422_));
 sky130_fd_sc_hd__a21oi_1 _1408_ (.A1(gate_cnt[12]),
    .A2(_0422_),
    .B1(gate_cnt[13]),
    .Y(_0423_));
 sky130_fd_sc_hd__nor3_1 _1409_ (.A(net13),
    .B(_0417_),
    .C(_0423_),
    .Y(_0173_));
 sky130_fd_sc_hd__o21ai_0 _1410_ (.A1(gate_cnt[12]),
    .A2(_0422_),
    .B1(_0348_),
    .Y(_0424_));
 sky130_fd_sc_hd__a21oi_1 _1411_ (.A1(gate_cnt[12]),
    .A2(_0422_),
    .B1(_0424_),
    .Y(_0174_));
 sky130_fd_sc_hd__o21ai_0 _1412_ (.A1(gate_cnt[11]),
    .A2(_0421_),
    .B1(_0348_),
    .Y(_0425_));
 sky130_fd_sc_hd__nor2_1 _1413_ (.A(_0422_),
    .B(_0425_),
    .Y(_0175_));
 sky130_fd_sc_hd__o21ai_0 _1414_ (.A1(gate_cnt[10]),
    .A2(_0416_),
    .B1(_0348_),
    .Y(_0426_));
 sky130_fd_sc_hd__nor2_1 _1415_ (.A(_0421_),
    .B(_0426_),
    .Y(_0176_));
 sky130_fd_sc_hd__nor2_1 _1416_ (.A(gate_cnt[9]),
    .B(_0415_),
    .Y(_0427_));
 sky130_fd_sc_hd__nor3_1 _1417_ (.A(net13),
    .B(_0416_),
    .C(_0427_),
    .Y(_0177_));
 sky130_fd_sc_hd__and2_2 _1418_ (.A(gate_cnt[6]),
    .B(_0391_),
    .X(_0428_));
 sky130_fd_sc_hd__a21oi_1 _1419_ (.A1(gate_cnt[7]),
    .A2(_0428_),
    .B1(gate_cnt[8]),
    .Y(_0429_));
 sky130_fd_sc_hd__nor3_1 _1420_ (.A(net13),
    .B(_0415_),
    .C(_0429_),
    .Y(_0178_));
 sky130_fd_sc_hd__o21ai_0 _1421_ (.A1(gate_cnt[7]),
    .A2(_0428_),
    .B1(_0348_),
    .Y(_0430_));
 sky130_fd_sc_hd__a21oi_1 _1422_ (.A1(gate_cnt[7]),
    .A2(_0428_),
    .B1(_0430_),
    .Y(_0179_));
 sky130_fd_sc_hd__nor2_1 _1423_ (.A(gate_cnt[6]),
    .B(_0391_),
    .Y(_0431_));
 sky130_fd_sc_hd__nor3_1 _1424_ (.A(net13),
    .B(_0428_),
    .C(_0431_),
    .Y(_0180_));
 sky130_fd_sc_hd__and2_2 _1425_ (.A(gate_cnt[3]),
    .B(_0390_),
    .X(_0432_));
 sky130_fd_sc_hd__a21oi_1 _1426_ (.A1(gate_cnt[4]),
    .A2(_0432_),
    .B1(gate_cnt[5]),
    .Y(_0433_));
 sky130_fd_sc_hd__nor3_1 _1427_ (.A(net13),
    .B(_0391_),
    .C(_0433_),
    .Y(_0181_));
 sky130_fd_sc_hd__o21ai_0 _1428_ (.A1(gate_cnt[4]),
    .A2(_0432_),
    .B1(_0348_),
    .Y(_0434_));
 sky130_fd_sc_hd__a21oi_1 _1429_ (.A1(gate_cnt[4]),
    .A2(_0432_),
    .B1(_0434_),
    .Y(_0182_));
 sky130_fd_sc_hd__nor2_1 _1430_ (.A(gate_cnt[3]),
    .B(_0390_),
    .Y(_0435_));
 sky130_fd_sc_hd__nor3_1 _1431_ (.A(net13),
    .B(_0432_),
    .C(_0435_),
    .Y(_0183_));
 sky130_fd_sc_hd__and3_2 _1432_ (.A(gate_cnt[1]),
    .B(gate_cnt[0]),
    .C(gate_en),
    .X(_0436_));
 sky130_fd_sc_hd__nor2_1 _1433_ (.A(gate_cnt[2]),
    .B(_0436_),
    .Y(_0437_));
 sky130_fd_sc_hd__nor3_1 _1434_ (.A(net13),
    .B(_0390_),
    .C(_0437_),
    .Y(_0184_));
 sky130_fd_sc_hd__a21oi_1 _1435_ (.A1(gate_cnt[0]),
    .A2(gate_en),
    .B1(gate_cnt[1]),
    .Y(_0438_));
 sky130_fd_sc_hd__nor3_1 _1436_ (.A(net13),
    .B(_0436_),
    .C(_0438_),
    .Y(_0185_));
 sky130_fd_sc_hd__xnor2_1 _1437_ (.A(gate_cnt[0]),
    .B(gate_en),
    .Y(_0439_));
 sky130_fd_sc_hd__nor2_1 _1438_ (.A(net13),
    .B(_0439_),
    .Y(_0186_));
 sky130_fd_sc_hd__nand3_1 _1439_ (.A(we),
    .B(_0648_),
    .C(net20),
    .Y(_0440_));
 sky130_fd_sc_hd__mux2_2 _1441_ (.A0(wdata[22]),
    .A1(\cal_r[1] [22]),
    .S(_0440_),
    .X(_0187_));
 sky130_fd_sc_hd__mux2_2 _1442_ (.A0(wdata[21]),
    .A1(\cal_r[1] [21]),
    .S(_0440_),
    .X(_0188_));
 sky130_fd_sc_hd__mux2_2 _1443_ (.A0(wdata[20]),
    .A1(\cal_r[1] [20]),
    .S(_0440_),
    .X(_0189_));
 sky130_fd_sc_hd__mux2_2 _1444_ (.A0(wdata[19]),
    .A1(\cal_r[1] [19]),
    .S(_0440_),
    .X(_0190_));
 sky130_fd_sc_hd__mux2_2 _1445_ (.A0(wdata[18]),
    .A1(\cal_r[1] [18]),
    .S(_0440_),
    .X(_0191_));
 sky130_fd_sc_hd__mux2_2 _1446_ (.A0(wdata[17]),
    .A1(\cal_r[1] [17]),
    .S(_0440_),
    .X(_0192_));
 sky130_fd_sc_hd__mux2_2 _1447_ (.A0(wdata[16]),
    .A1(\cal_r[1] [16]),
    .S(_0440_),
    .X(_0193_));
 sky130_fd_sc_hd__mux2_2 _1448_ (.A0(wdata[15]),
    .A1(\cal_r[1] [15]),
    .S(_0440_),
    .X(_0194_));
 sky130_fd_sc_hd__mux2_2 _1449_ (.A0(wdata[14]),
    .A1(\cal_r[1] [14]),
    .S(_0440_),
    .X(_0195_));
 sky130_fd_sc_hd__mux2_2 _1450_ (.A0(wdata[13]),
    .A1(\cal_r[1] [13]),
    .S(_0440_),
    .X(_0196_));
 sky130_fd_sc_hd__mux2_2 _1452_ (.A0(wdata[12]),
    .A1(\cal_r[1] [12]),
    .S(_0440_),
    .X(_0197_));
 sky130_fd_sc_hd__mux2_2 _1453_ (.A0(wdata[11]),
    .A1(\cal_r[1] [11]),
    .S(_0440_),
    .X(_0198_));
 sky130_fd_sc_hd__mux2_2 _1454_ (.A0(wdata[10]),
    .A1(\cal_r[1] [10]),
    .S(_0440_),
    .X(_0199_));
 sky130_fd_sc_hd__mux2_2 _1455_ (.A0(wdata[3]),
    .A1(ctrl_sel[2]),
    .S(_0313_),
    .X(_0200_));
 sky130_fd_sc_hd__mux2_2 _1456_ (.A0(cnt_o[23]),
    .A1(\count_r[1] [23]),
    .S(_0356_),
    .X(_0201_));
 sky130_fd_sc_hd__mux2_2 _1457_ (.A0(wdata[9]),
    .A1(\cal_r[1] [9]),
    .S(_0440_),
    .X(_0202_));
 sky130_fd_sc_hd__mux2_2 _1458_ (.A0(cnt_o[23]),
    .A1(\count_r[3] [23]),
    .S(net12),
    .X(_0203_));
 sky130_fd_sc_hd__nand2_1 _1459_ (.A(wdata[3]),
    .B(net13),
    .Y(_0443_));
 sky130_fd_sc_hd__nand2_1 _1460_ (.A(sel_q[2]),
    .B(_0348_),
    .Y(_0444_));
 sky130_fd_sc_hd__nand2_1 _1461_ (.A(_0443_),
    .B(_0444_),
    .Y(_0204_));
 sky130_fd_sc_hd__mux2_2 _1462_ (.A0(cnt_o[23]),
    .A1(\count_r[2] [23]),
    .S(_0344_),
    .X(_0205_));
 sky130_fd_sc_hd__mux2_2 _1463_ (.A0(wdata[23]),
    .A1(\cal_r[0] [23]),
    .S(_0339_),
    .X(_0206_));
 sky130_fd_sc_hd__nor2_1 _1464_ (.A(k_q[4]),
    .B(net13),
    .Y(_0445_));
 sky130_fd_sc_hd__nor2_1 _1465_ (.A(wdata[8]),
    .B(_0348_),
    .Y(_0446_));
 sky130_fd_sc_hd__nor2_1 _1466_ (.A(_0445_),
    .B(_0446_),
    .Y(_0207_));
 sky130_fd_sc_hd__mux2_2 _1467_ (.A0(wdata[8]),
    .A1(ctrl_k[4]),
    .S(_0313_),
    .X(_0208_));
 sky130_fd_sc_hd__nand2_1 _1468_ (.A(_0332_),
    .B(_0343_),
    .Y(_0447_));
 sky130_fd_sc_hd__mux2_2 _1470_ (.A0(cnt_o[23]),
    .A1(\count_r[0] [23]),
    .S(_0447_),
    .X(_0209_));
 sky130_fd_sc_hd__inv_1 _1471_ (.A(busy_r),
    .Y(_0449_));
 sky130_fd_sc_hd__o21ai_0 _1472_ (.A1(_0449_),
    .A2(_0343_),
    .B1(_0348_),
    .Y(_0210_));
 sky130_fd_sc_hd__mux2_2 _1473_ (.A0(wdata[8]),
    .A1(\cal_r[1] [8]),
    .S(_0440_),
    .X(_0211_));
 sky130_fd_sc_hd__a21o_1 _1474_ (.A1(done_r),
    .A2(_0348_),
    .B1(_0343_),
    .X(_0212_));
 sky130_fd_sc_hd__nand3_1 _1475_ (.A(we),
    .B(net22),
    .C(_0648_),
    .Y(_0450_));
 sky130_fd_sc_hd__mux2_2 _1477_ (.A0(wdata[23]),
    .A1(\cal_r[4] [23]),
    .S(_0450_),
    .X(_0213_));
 sky130_fd_sc_hd__mux2_2 _1478_ (.A0(wdata[23]),
    .A1(\cal_r[1] [23]),
    .S(_0440_),
    .X(_0214_));
 sky130_fd_sc_hd__inv_1 _1479_ (.A(ovf_o),
    .Y(_0452_));
 sky130_fd_sc_hd__a21oi_1 _1480_ (.A1(ovf_r),
    .A2(_0348_),
    .B1(_0343_),
    .Y(_0453_));
 sky130_fd_sc_hd__a21oi_1 _1481_ (.A1(_0452_),
    .A2(_0343_),
    .B1(_0453_),
    .Y(_0215_));
 sky130_fd_sc_hd__mux2_2 _1482_ (.A0(wdata[7]),
    .A1(\cal_r[1] [7]),
    .S(_0440_),
    .X(_0216_));
 sky130_fd_sc_hd__mux2_2 _1483_ (.A0(wdata[6]),
    .A1(\cal_r[1] [6]),
    .S(_0440_),
    .X(_0217_));
 sky130_fd_sc_hd__mux2_2 _1484_ (.A0(wdata[5]),
    .A1(\cal_r[1] [5]),
    .S(_0440_),
    .X(_0218_));
 sky130_fd_sc_hd__nand2_1 _1485_ (.A(gate_cnt[30]),
    .B(_0381_),
    .Y(_0454_));
 sky130_fd_sc_hd__xor2_1 _1486_ (.A(gate_cnt[31]),
    .B(_0454_),
    .X(_0455_));
 sky130_fd_sc_hd__nor2_1 _1487_ (.A(net13),
    .B(_0455_),
    .Y(_0219_));
 sky130_fd_sc_hd__mux2_2 _1488_ (.A0(wdata[23]),
    .A1(\cal_r[3] [23]),
    .S(_0365_),
    .X(_0220_));
 sky130_fd_sc_hd__mux2_2 _1489_ (.A0(wdata[4]),
    .A1(\cal_r[1] [4]),
    .S(_0440_),
    .X(_0221_));
 sky130_fd_sc_hd__mux2_2 _1490_ (.A0(wdata[3]),
    .A1(\cal_r[1] [3]),
    .S(_0440_),
    .X(_0222_));
 sky130_fd_sc_hd__mux2_2 _1491_ (.A0(wdata[2]),
    .A1(\cal_r[1] [2]),
    .S(_0440_),
    .X(_0223_));
 sky130_fd_sc_hd__mux2_2 _1492_ (.A0(wdata[1]),
    .A1(\cal_r[1] [1]),
    .S(_0440_),
    .X(_0224_));
 sky130_fd_sc_hd__mux2_2 _1493_ (.A0(wdata[0]),
    .A1(\cal_r[1] [0]),
    .S(_0440_),
    .X(_0225_));
 sky130_fd_sc_hd__mux2_2 _1494_ (.A0(wdata[22]),
    .A1(\cal_r[4] [22]),
    .S(net10),
    .X(_0226_));
 sky130_fd_sc_hd__mux2_2 _1495_ (.A0(wdata[21]),
    .A1(\cal_r[4] [21]),
    .S(_0450_),
    .X(_0227_));
 sky130_fd_sc_hd__mux2_2 _1496_ (.A0(wdata[20]),
    .A1(\cal_r[4] [20]),
    .S(_0450_),
    .X(_0228_));
 sky130_fd_sc_hd__mux2_2 _1497_ (.A0(wdata[19]),
    .A1(\cal_r[4] [19]),
    .S(net10),
    .X(_0229_));
 sky130_fd_sc_hd__mux2_2 _1498_ (.A0(wdata[18]),
    .A1(\cal_r[4] [18]),
    .S(net10),
    .X(_0230_));
 sky130_fd_sc_hd__mux2_2 _1499_ (.A0(wdata[17]),
    .A1(\cal_r[4] [17]),
    .S(net10),
    .X(_0231_));
 sky130_fd_sc_hd__mux2_2 _1500_ (.A0(wdata[16]),
    .A1(\cal_r[4] [16]),
    .S(_0450_),
    .X(_0232_));
 sky130_fd_sc_hd__mux2_2 _1501_ (.A0(wdata[15]),
    .A1(\cal_r[4] [15]),
    .S(net10),
    .X(_0233_));
 sky130_fd_sc_hd__mux2_2 _1502_ (.A0(wdata[14]),
    .A1(\cal_r[4] [14]),
    .S(_0450_),
    .X(_0234_));
 sky130_fd_sc_hd__mux2_2 _1504_ (.A0(wdata[13]),
    .A1(\cal_r[4] [13]),
    .S(_0450_),
    .X(_0235_));
 sky130_fd_sc_hd__mux2_2 _1505_ (.A0(wdata[12]),
    .A1(\cal_r[4] [12]),
    .S(net10),
    .X(_0236_));
 sky130_fd_sc_hd__mux2_2 _1506_ (.A0(wdata[11]),
    .A1(\cal_r[4] [11]),
    .S(net10),
    .X(_0237_));
 sky130_fd_sc_hd__mux2_2 _1507_ (.A0(wdata[10]),
    .A1(\cal_r[4] [10]),
    .S(net10),
    .X(_0238_));
 sky130_fd_sc_hd__mux2_2 _1508_ (.A0(wdata[9]),
    .A1(\cal_r[4] [9]),
    .S(_0450_),
    .X(_0239_));
 sky130_fd_sc_hd__mux2_2 _1509_ (.A0(wdata[8]),
    .A1(\cal_r[4] [8]),
    .S(net10),
    .X(_0240_));
 sky130_fd_sc_hd__mux2_2 _1510_ (.A0(wdata[7]),
    .A1(\cal_r[4] [7]),
    .S(net10),
    .X(_0241_));
 sky130_fd_sc_hd__mux2_2 _1511_ (.A0(wdata[6]),
    .A1(\cal_r[4] [6]),
    .S(net10),
    .X(_0242_));
 sky130_fd_sc_hd__mux2_2 _1512_ (.A0(wdata[5]),
    .A1(\cal_r[4] [5]),
    .S(_0450_),
    .X(_0243_));
 sky130_fd_sc_hd__mux2_2 _1513_ (.A0(wdata[4]),
    .A1(\cal_r[4] [4]),
    .S(net10),
    .X(_0244_));
 sky130_fd_sc_hd__mux2_2 _1514_ (.A0(wdata[3]),
    .A1(\cal_r[4] [3]),
    .S(net10),
    .X(_0245_));
 sky130_fd_sc_hd__mux2_2 _1515_ (.A0(wdata[2]),
    .A1(\cal_r[4] [2]),
    .S(net10),
    .X(_0246_));
 sky130_fd_sc_hd__mux2_2 _1516_ (.A0(wdata[1]),
    .A1(\cal_r[4] [1]),
    .S(net10),
    .X(_0247_));
 sky130_fd_sc_hd__mux2_2 _1517_ (.A0(wdata[0]),
    .A1(\cal_r[4] [0]),
    .S(net10),
    .X(_0248_));
 sky130_fd_sc_hd__mux2_2 _1518_ (.A0(cnt_o[22]),
    .A1(\count_r[0] [22]),
    .S(_0447_),
    .X(_0249_));
 sky130_fd_sc_hd__mux2_2 _1519_ (.A0(cnt_o[21]),
    .A1(\count_r[0] [21]),
    .S(_0447_),
    .X(_0250_));
 sky130_fd_sc_hd__mux2_2 _1520_ (.A0(cnt_o[20]),
    .A1(\count_r[0] [20]),
    .S(_0447_),
    .X(_0251_));
 sky130_fd_sc_hd__mux2_2 _1521_ (.A0(cnt_o[19]),
    .A1(\count_r[0] [19]),
    .S(_0447_),
    .X(_0252_));
 sky130_fd_sc_hd__mux2_2 _1522_ (.A0(cnt_o[18]),
    .A1(\count_r[0] [18]),
    .S(_0447_),
    .X(_0253_));
 sky130_fd_sc_hd__mux2_2 _1523_ (.A0(cnt_o[17]),
    .A1(\count_r[0] [17]),
    .S(_0447_),
    .X(_0254_));
 sky130_fd_sc_hd__mux2_2 _1524_ (.A0(cnt_o[16]),
    .A1(\count_r[0] [16]),
    .S(_0447_),
    .X(_0255_));
 sky130_fd_sc_hd__mux2_2 _1525_ (.A0(cnt_o[15]),
    .A1(\count_r[0] [15]),
    .S(_0447_),
    .X(_0256_));
 sky130_fd_sc_hd__mux2_2 _1526_ (.A0(cnt_o[14]),
    .A1(\count_r[0] [14]),
    .S(_0447_),
    .X(_0257_));
 sky130_fd_sc_hd__mux2_2 _1528_ (.A0(cnt_o[13]),
    .A1(\count_r[0] [13]),
    .S(_0447_),
    .X(_0258_));
 sky130_fd_sc_hd__mux2_2 _1529_ (.A0(cnt_o[12]),
    .A1(\count_r[0] [12]),
    .S(_0447_),
    .X(_0259_));
 sky130_fd_sc_hd__mux2_2 _1530_ (.A0(cnt_o[11]),
    .A1(\count_r[0] [11]),
    .S(_0447_),
    .X(_0260_));
 sky130_fd_sc_hd__mux2_2 _1531_ (.A0(cnt_o[10]),
    .A1(\count_r[0] [10]),
    .S(_0447_),
    .X(_0261_));
 sky130_fd_sc_hd__mux2_2 _1532_ (.A0(cnt_o[23]),
    .A1(\count_r[4] [23]),
    .S(_0362_),
    .X(_0262_));
 sky130_fd_sc_hd__mux2_2 _1533_ (.A0(cnt_o[9]),
    .A1(\count_r[0] [9]),
    .S(_0447_),
    .X(_0263_));
 sky130_fd_sc_hd__mux2_2 _1534_ (.A0(cnt_o[8]),
    .A1(\count_r[0] [8]),
    .S(_0447_),
    .X(_0264_));
 sky130_fd_sc_hd__mux2_2 _1535_ (.A0(cnt_o[7]),
    .A1(\count_r[0] [7]),
    .S(_0447_),
    .X(_0265_));
 sky130_fd_sc_hd__mux2_2 _1536_ (.A0(cnt_o[6]),
    .A1(\count_r[0] [6]),
    .S(_0447_),
    .X(_0266_));
 sky130_fd_sc_hd__mux2_2 _1537_ (.A0(cnt_o[5]),
    .A1(\count_r[0] [5]),
    .S(_0447_),
    .X(_0267_));
 sky130_fd_sc_hd__mux2_2 _1538_ (.A0(cnt_o[4]),
    .A1(\count_r[0] [4]),
    .S(_0447_),
    .X(_0268_));
 sky130_fd_sc_hd__mux2_2 _1539_ (.A0(cnt_o[3]),
    .A1(\count_r[0] [3]),
    .S(_0447_),
    .X(_0269_));
 sky130_fd_sc_hd__mux2_2 _1540_ (.A0(wdata[23]),
    .A1(\cal_r[2] [23]),
    .S(net11),
    .X(_0270_));
 sky130_fd_sc_hd__mux2_2 _1541_ (.A0(cnt_o[2]),
    .A1(\count_r[0] [2]),
    .S(_0447_),
    .X(_0271_));
 sky130_fd_sc_hd__mux2_2 _1542_ (.A0(cnt_o[1]),
    .A1(\count_r[0] [1]),
    .S(_0447_),
    .X(_0272_));
 sky130_fd_sc_hd__mux2_2 _1543_ (.A0(cnt_o[0]),
    .A1(\count_r[0] [0]),
    .S(_0447_),
    .X(_0273_));
 sky130_fd_sc_hd__mux2_2 _1544_ (.A0(wdata[7]),
    .A1(ctrl_k[3]),
    .S(_0313_),
    .X(_0274_));
 sky130_fd_sc_hd__mux2_2 _1545_ (.A0(wdata[6]),
    .A1(ctrl_k[2]),
    .S(_0313_),
    .X(_0275_));
 sky130_fd_sc_hd__mux2_2 _1546_ (.A0(wdata[5]),
    .A1(ctrl_k[1]),
    .S(_0313_),
    .X(_0276_));
 sky130_fd_sc_hd__mux2_2 _1547_ (.A0(wdata[4]),
    .A1(ctrl_k[0]),
    .S(_0313_),
    .X(_0277_));
 sky130_fd_sc_hd__nand2_1 _1548_ (.A(wdata[7]),
    .B(net13),
    .Y(_0458_));
 sky130_fd_sc_hd__nand2_1 _1549_ (.A(k_q[3]),
    .B(_0348_),
    .Y(_0459_));
 sky130_fd_sc_hd__nand2_1 _1550_ (.A(_0458_),
    .B(_0459_),
    .Y(_0278_));
 sky130_fd_sc_hd__nand2_1 _1551_ (.A(wdata[6]),
    .B(net13),
    .Y(_0460_));
 sky130_fd_sc_hd__nand2_1 _1552_ (.A(k_q[2]),
    .B(_0348_),
    .Y(_0461_));
 sky130_fd_sc_hd__nand2_1 _1553_ (.A(_0460_),
    .B(_0461_),
    .Y(_0279_));
 sky130_fd_sc_hd__nand2_1 _1554_ (.A(wdata[5]),
    .B(net13),
    .Y(_0462_));
 sky130_fd_sc_hd__nand2_1 _1555_ (.A(k_q[1]),
    .B(_0348_),
    .Y(_0463_));
 sky130_fd_sc_hd__nand2_1 _1556_ (.A(_0462_),
    .B(_0463_),
    .Y(_0280_));
 sky130_fd_sc_hd__nand2_1 _1557_ (.A(wdata[4]),
    .B(net13),
    .Y(_0464_));
 sky130_fd_sc_hd__nand2_1 _1558_ (.A(k_q[0]),
    .B(_0348_),
    .Y(_0465_));
 sky130_fd_sc_hd__nand2_1 _1559_ (.A(_0464_),
    .B(_0465_),
    .Y(_0281_));
 sky130_fd_sc_hd__mux2_2 _1560_ (.A0(wdata[22]),
    .A1(\cal_r[0] [22]),
    .S(_0339_),
    .X(_0282_));
 sky130_fd_sc_hd__mux2_2 _1561_ (.A0(wdata[21]),
    .A1(\cal_r[0] [21]),
    .S(_0339_),
    .X(_0283_));
 sky130_fd_sc_hd__mux2_2 _1562_ (.A0(wdata[20]),
    .A1(\cal_r[0] [20]),
    .S(_0339_),
    .X(_0284_));
 sky130_fd_sc_hd__mux2_2 _1563_ (.A0(wdata[19]),
    .A1(\cal_r[0] [19]),
    .S(_0339_),
    .X(_0285_));
 sky130_fd_sc_hd__mux2_2 _1564_ (.A0(wdata[18]),
    .A1(\cal_r[0] [18]),
    .S(_0339_),
    .X(_0286_));
 sky130_fd_sc_hd__mux2_2 _1565_ (.A0(wdata[17]),
    .A1(\cal_r[0] [17]),
    .S(_0339_),
    .X(_0287_));
 sky130_fd_sc_hd__mux2_2 _1566_ (.A0(wdata[16]),
    .A1(\cal_r[0] [16]),
    .S(_0339_),
    .X(_0288_));
 sky130_fd_sc_hd__mux2_2 _1567_ (.A0(wdata[15]),
    .A1(\cal_r[0] [15]),
    .S(_0339_),
    .X(_0289_));
 sky130_fd_sc_hd__mux2_2 _1568_ (.A0(wdata[14]),
    .A1(\cal_r[0] [14]),
    .S(_0339_),
    .X(_0290_));
 sky130_fd_sc_hd__mux2_2 _1569_ (.A0(wdata[13]),
    .A1(\cal_r[0] [13]),
    .S(_0339_),
    .X(_0291_));
 sky130_fd_sc_hd__dfrtp_1 _1570_ (.CLK(clknet_leaf_5_clk_ref),
    .D(_0086_),
    .RESET_B(rst_n),
    .Q(ctrl_sel[0]));
 sky130_fd_sc_hd__dfrtp_1 _1571_ (.CLK(clknet_leaf_4_clk_ref),
    .D(_0085_),
    .RESET_B(rst_n),
    .Q(ctrl_sel[1]));
 sky130_fd_sc_hd__dfrtp_1 _1572_ (.CLK(clknet_leaf_4_clk_ref),
    .D(_0200_),
    .RESET_B(rst_n),
    .Q(ctrl_sel[2]));
 sky130_fd_sc_hd__dfrtp_1 _1573_ (.CLK(clknet_leaf_32_clk_ref),
    .D(_0084_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [0]));
 sky130_fd_sc_hd__dfrtp_1 _1574_ (.CLK(clknet_leaf_15_clk_ref),
    .D(_0083_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [1]));
 sky130_fd_sc_hd__dfrtp_1 _1575_ (.CLK(clknet_leaf_15_clk_ref),
    .D(_0082_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [2]));
 sky130_fd_sc_hd__dfrtp_1 _1576_ (.CLK(clknet_leaf_22_clk_ref),
    .D(_0081_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [3]));
 sky130_fd_sc_hd__dfrtp_1 _1577_ (.CLK(clknet_leaf_25_clk_ref),
    .D(_0080_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [4]));
 sky130_fd_sc_hd__dfrtp_1 _1578_ (.CLK(clknet_leaf_25_clk_ref),
    .D(_0079_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [5]));
 sky130_fd_sc_hd__dfrtp_1 _1579_ (.CLK(clknet_leaf_22_clk_ref),
    .D(_0078_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [6]));
 sky130_fd_sc_hd__dfrtp_1 _1580_ (.CLK(clknet_leaf_23_clk_ref),
    .D(_0077_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [7]));
 sky130_fd_sc_hd__dfrtp_1 _1581_ (.CLK(clknet_leaf_21_clk_ref),
    .D(_0076_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [8]));
 sky130_fd_sc_hd__dfrtp_1 _1582_ (.CLK(clknet_leaf_26_clk_ref),
    .D(_0075_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [9]));
 sky130_fd_sc_hd__dfrtp_1 _1583_ (.CLK(clknet_leaf_15_clk_ref),
    .D(_0074_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [10]));
 sky130_fd_sc_hd__dfrtp_1 _1584_ (.CLK(clknet_leaf_27_clk_ref),
    .D(_0073_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [11]));
 sky130_fd_sc_hd__dfrtp_1 _1585_ (.CLK(clknet_leaf_31_clk_ref),
    .D(_0072_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [12]));
 sky130_fd_sc_hd__dfrtp_1 _1586_ (.CLK(clknet_leaf_28_clk_ref),
    .D(_0071_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [13]));
 sky130_fd_sc_hd__dfrtp_1 _1587_ (.CLK(clknet_leaf_30_clk_ref),
    .D(_0070_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [14]));
 sky130_fd_sc_hd__dfrtp_1 _1588_ (.CLK(clknet_leaf_29_clk_ref),
    .D(_0069_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [15]));
 sky130_fd_sc_hd__dfrtp_1 _1589_ (.CLK(clknet_leaf_35_clk_ref),
    .D(_0068_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [16]));
 sky130_fd_sc_hd__dfrtp_1 _1590_ (.CLK(clknet_leaf_33_clk_ref),
    .D(_0067_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [17]));
 sky130_fd_sc_hd__dfrtp_1 _1591_ (.CLK(clknet_leaf_34_clk_ref),
    .D(_0066_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [18]));
 sky130_fd_sc_hd__dfrtp_1 _1592_ (.CLK(clknet_leaf_29_clk_ref),
    .D(_0065_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [19]));
 sky130_fd_sc_hd__dfrtp_1 _1593_ (.CLK(clknet_leaf_33_clk_ref),
    .D(_0064_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [20]));
 sky130_fd_sc_hd__dfrtp_1 _1594_ (.CLK(clknet_leaf_33_clk_ref),
    .D(_0063_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [21]));
 sky130_fd_sc_hd__dfrtp_1 _1595_ (.CLK(clknet_leaf_31_clk_ref),
    .D(_0062_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [22]));
 sky130_fd_sc_hd__dfrtp_1 _1596_ (.CLK(clknet_leaf_26_clk_ref),
    .D(_0201_),
    .RESET_B(rst_n),
    .Q(\count_r[1] [23]));
 sky130_fd_sc_hd__dfrtp_1 _1597_ (.CLK(clknet_leaf_32_clk_ref),
    .D(_0061_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [0]));
 sky130_fd_sc_hd__dfrtp_1 _1598_ (.CLK(clknet_leaf_3_clk_ref),
    .D(_0060_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [1]));
 sky130_fd_sc_hd__dfrtp_1 _1599_ (.CLK(clknet_leaf_15_clk_ref),
    .D(_0059_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [2]));
 sky130_fd_sc_hd__dfrtp_1 _1600_ (.CLK(clknet_leaf_22_clk_ref),
    .D(_0058_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [3]));
 sky130_fd_sc_hd__dfrtp_1 _1601_ (.CLK(clknet_leaf_21_clk_ref),
    .D(_0057_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [4]));
 sky130_fd_sc_hd__dfrtp_1 _1602_ (.CLK(clknet_leaf_25_clk_ref),
    .D(_0056_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [5]));
 sky130_fd_sc_hd__dfrtp_1 _1603_ (.CLK(clknet_leaf_23_clk_ref),
    .D(_0055_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [6]));
 sky130_fd_sc_hd__dfrtp_1 _1604_ (.CLK(clknet_leaf_23_clk_ref),
    .D(_0054_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [7]));
 sky130_fd_sc_hd__dfrtp_1 _1605_ (.CLK(clknet_leaf_20_clk_ref),
    .D(_0053_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [8]));
 sky130_fd_sc_hd__dfrtp_1 _1606_ (.CLK(clknet_leaf_26_clk_ref),
    .D(_0052_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [9]));
 sky130_fd_sc_hd__dfrtp_1 _1607_ (.CLK(clknet_leaf_15_clk_ref),
    .D(_0051_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [10]));
 sky130_fd_sc_hd__dfrtp_1 _1608_ (.CLK(clknet_leaf_26_clk_ref),
    .D(_0050_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [11]));
 sky130_fd_sc_hd__dfrtp_1 _1609_ (.CLK(clknet_leaf_31_clk_ref),
    .D(_0049_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [12]));
 sky130_fd_sc_hd__dfrtp_1 _1610_ (.CLK(clknet_leaf_27_clk_ref),
    .D(_0048_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [13]));
 sky130_fd_sc_hd__dfrtp_1 _1611_ (.CLK(clknet_leaf_30_clk_ref),
    .D(_0047_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [14]));
 sky130_fd_sc_hd__dfrtp_1 _1612_ (.CLK(clknet_leaf_29_clk_ref),
    .D(_0046_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [15]));
 sky130_fd_sc_hd__dfrtp_1 _1613_ (.CLK(clknet_leaf_35_clk_ref),
    .D(_0045_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [16]));
 sky130_fd_sc_hd__dfrtp_1 _1614_ (.CLK(clknet_leaf_33_clk_ref),
    .D(_0044_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [17]));
 sky130_fd_sc_hd__dfrtp_1 _1615_ (.CLK(clknet_leaf_34_clk_ref),
    .D(_0043_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [18]));
 sky130_fd_sc_hd__dfrtp_1 _1616_ (.CLK(clknet_leaf_29_clk_ref),
    .D(_0042_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [19]));
 sky130_fd_sc_hd__dfrtp_1 _1617_ (.CLK(clknet_leaf_34_clk_ref),
    .D(_0041_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [20]));
 sky130_fd_sc_hd__dfrtp_1 _1618_ (.CLK(clknet_leaf_32_clk_ref),
    .D(_0040_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [21]));
 sky130_fd_sc_hd__dfrtp_1 _1619_ (.CLK(clknet_leaf_30_clk_ref),
    .D(_0039_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [22]));
 sky130_fd_sc_hd__dfrtp_1 _1620_ (.CLK(clknet_leaf_27_clk_ref),
    .D(_0203_),
    .RESET_B(rst_n),
    .Q(\count_r[3] [23]));
 sky130_fd_sc_hd__dfrtp_1 _1621_ (.CLK(clknet_leaf_4_clk_ref),
    .D(_0038_),
    .RESET_B(rst_n),
    .Q(sel_q[0]));
 sky130_fd_sc_hd__dfrtp_1 _1622_ (.CLK(clknet_leaf_3_clk_ref),
    .D(_0037_),
    .RESET_B(rst_n),
    .Q(sel_q[1]));
 sky130_fd_sc_hd__dfrtp_1 _1623_ (.CLK(clknet_leaf_3_clk_ref),
    .D(_0204_),
    .RESET_B(rst_n),
    .Q(sel_q[2]));
 sky130_fd_sc_hd__dfrtp_1 _1624_ (.CLK(clknet_leaf_3_clk_ref),
    .D(_0036_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [0]));
 sky130_fd_sc_hd__dfrtp_1 _1625_ (.CLK(clknet_leaf_15_clk_ref),
    .D(_0035_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [1]));
 sky130_fd_sc_hd__dfrtp_1 _1626_ (.CLK(clknet_leaf_24_clk_ref),
    .D(_0034_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [2]));
 sky130_fd_sc_hd__dfrtp_1 _1627_ (.CLK(clknet_leaf_21_clk_ref),
    .D(_0033_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [3]));
 sky130_fd_sc_hd__dfrtp_1 _1628_ (.CLK(clknet_leaf_25_clk_ref),
    .D(_0032_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [4]));
 sky130_fd_sc_hd__dfrtp_1 _1629_ (.CLK(clknet_leaf_25_clk_ref),
    .D(_0031_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [5]));
 sky130_fd_sc_hd__dfrtp_1 _1630_ (.CLK(clknet_leaf_22_clk_ref),
    .D(_0030_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [6]));
 sky130_fd_sc_hd__dfrtp_1 _1631_ (.CLK(clknet_leaf_23_clk_ref),
    .D(_0029_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [7]));
 sky130_fd_sc_hd__dfrtp_1 _1632_ (.CLK(clknet_leaf_21_clk_ref),
    .D(_0028_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [8]));
 sky130_fd_sc_hd__dfrtp_1 _1633_ (.CLK(clknet_leaf_26_clk_ref),
    .D(_0027_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [9]));
 sky130_fd_sc_hd__dfrtp_1 _1634_ (.CLK(clknet_leaf_24_clk_ref),
    .D(_0026_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [10]));
 sky130_fd_sc_hd__dfrtp_1 _1635_ (.CLK(clknet_leaf_27_clk_ref),
    .D(_0025_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [11]));
 sky130_fd_sc_hd__dfrtp_1 _1636_ (.CLK(clknet_leaf_32_clk_ref),
    .D(_0024_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [12]));
 sky130_fd_sc_hd__dfrtp_1 _1637_ (.CLK(clknet_leaf_27_clk_ref),
    .D(_0023_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [13]));
 sky130_fd_sc_hd__dfrtp_1 _1638_ (.CLK(clknet_leaf_30_clk_ref),
    .D(_0022_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [14]));
 sky130_fd_sc_hd__dfrtp_1 _1639_ (.CLK(clknet_leaf_31_clk_ref),
    .D(_0021_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [15]));
 sky130_fd_sc_hd__dfrtp_1 _1640_ (.CLK(clknet_leaf_35_clk_ref),
    .D(_0020_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [16]));
 sky130_fd_sc_hd__dfrtp_1 _1641_ (.CLK(clknet_leaf_34_clk_ref),
    .D(_0019_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [17]));
 sky130_fd_sc_hd__dfrtp_1 _1642_ (.CLK(clknet_leaf_30_clk_ref),
    .D(_0018_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [18]));
 sky130_fd_sc_hd__dfrtp_1 _1643_ (.CLK(clknet_leaf_28_clk_ref),
    .D(_0017_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [19]));
 sky130_fd_sc_hd__dfrtp_1 _1644_ (.CLK(clknet_leaf_30_clk_ref),
    .D(_0016_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [20]));
 sky130_fd_sc_hd__dfrtp_1 _1645_ (.CLK(clknet_leaf_34_clk_ref),
    .D(_0015_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [21]));
 sky130_fd_sc_hd__dfrtp_1 _1646_ (.CLK(clknet_leaf_31_clk_ref),
    .D(_0014_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [22]));
 sky130_fd_sc_hd__dfrtp_1 _1647_ (.CLK(clknet_leaf_26_clk_ref),
    .D(_0205_),
    .RESET_B(rst_n),
    .Q(\count_r[2] [23]));
 sky130_fd_sc_hd__dfrtp_1 _1648_ (.CLK(clknet_leaf_0_clk_ref),
    .D(_0013_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [0]));
 sky130_fd_sc_hd__dfrtp_1 _1649_ (.CLK(clknet_leaf_5_clk_ref),
    .D(_0012_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [1]));
 sky130_fd_sc_hd__dfrtp_1 _1650_ (.CLK(clknet_leaf_6_clk_ref),
    .D(_0011_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [2]));
 sky130_fd_sc_hd__dfrtp_1 _1651_ (.CLK(clknet_leaf_4_clk_ref),
    .D(_0010_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [3]));
 sky130_fd_sc_hd__dfrtp_1 _1652_ (.CLK(clknet_leaf_7_clk_ref),
    .D(_0009_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [4]));
 sky130_fd_sc_hd__dfrtp_1 _1653_ (.CLK(clknet_leaf_2_clk_ref),
    .D(_0008_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [5]));
 sky130_fd_sc_hd__dfrtp_1 _1654_ (.CLK(clknet_leaf_14_clk_ref),
    .D(_0007_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [6]));
 sky130_fd_sc_hd__dfrtp_1 _1655_ (.CLK(clknet_leaf_11_clk_ref),
    .D(_0006_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [7]));
 sky130_fd_sc_hd__dfrtp_1 _1656_ (.CLK(clknet_leaf_11_clk_ref),
    .D(_0005_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [8]));
 sky130_fd_sc_hd__dfrtp_1 _1657_ (.CLK(clknet_leaf_36_clk_ref),
    .D(_0004_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [9]));
 sky130_fd_sc_hd__dfrtp_1 _1658_ (.CLK(clknet_leaf_8_clk_ref),
    .D(_0003_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [10]));
 sky130_fd_sc_hd__dfrtp_1 _1659_ (.CLK(clknet_leaf_10_clk_ref),
    .D(_0002_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [11]));
 sky130_fd_sc_hd__dfrtp_1 _1660_ (.CLK(clknet_leaf_40_clk_ref),
    .D(_0001_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [12]));
 sky130_fd_sc_hd__dfrtp_1 _1661_ (.CLK(clknet_leaf_38_clk_ref),
    .D(_0291_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [13]));
 sky130_fd_sc_hd__dfrtp_1 _1662_ (.CLK(clknet_leaf_37_clk_ref),
    .D(_0290_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [14]));
 sky130_fd_sc_hd__dfrtp_1 _1663_ (.CLK(clknet_leaf_6_clk_ref),
    .D(_0289_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [15]));
 sky130_fd_sc_hd__dfrtp_1 _1664_ (.CLK(clknet_leaf_36_clk_ref),
    .D(_0288_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [16]));
 sky130_fd_sc_hd__dfrtp_1 _1665_ (.CLK(clknet_leaf_0_clk_ref),
    .D(_0287_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [17]));
 sky130_fd_sc_hd__dfrtp_1 _1666_ (.CLK(clknet_leaf_10_clk_ref),
    .D(_0286_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [18]));
 sky130_fd_sc_hd__dfrtp_1 _1667_ (.CLK(clknet_leaf_8_clk_ref),
    .D(_0285_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [19]));
 sky130_fd_sc_hd__dfrtp_1 _1668_ (.CLK(clknet_leaf_39_clk_ref),
    .D(_0284_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [20]));
 sky130_fd_sc_hd__dfrtp_1 _1669_ (.CLK(clknet_leaf_40_clk_ref),
    .D(_0283_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [21]));
 sky130_fd_sc_hd__dfrtp_1 _1670_ (.CLK(clknet_leaf_8_clk_ref),
    .D(_0282_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [22]));
 sky130_fd_sc_hd__dfrtp_1 _1671_ (.CLK(clknet_leaf_38_clk_ref),
    .D(_0206_),
    .RESET_B(rst_n),
    .Q(\cal_r[0] [23]));
 sky130_fd_sc_hd__dfrtp_1 _1672_ (.CLK(clknet_leaf_13_clk_ref),
    .D(_0281_),
    .RESET_B(rst_n),
    .Q(k_q[0]));
 sky130_fd_sc_hd__dfstp_2 _1673_ (.CLK(clknet_leaf_16_clk_ref),
    .D(_0280_),
    .SET_B(rst_n),
    .Q(k_q[1]));
 sky130_fd_sc_hd__dfrtp_1 _1674_ (.CLK(clknet_leaf_16_clk_ref),
    .D(_0279_),
    .RESET_B(rst_n),
    .Q(k_q[2]));
 sky130_fd_sc_hd__dfstp_2 _1675_ (.CLK(clknet_leaf_12_clk_ref),
    .D(_0278_),
    .SET_B(rst_n),
    .Q(k_q[3]));
 sky130_fd_sc_hd__dfrtp_1 _1676_ (.CLK(clknet_leaf_16_clk_ref),
    .D(_0207_),
    .RESET_B(rst_n),
    .Q(k_q[4]));
 sky130_fd_sc_hd__dfrtp_1 _1677_ (.CLK(clknet_leaf_3_clk_ref),
    .D(_0277_),
    .RESET_B(rst_n),
    .Q(ctrl_k[0]));
 sky130_fd_sc_hd__dfstp_2 _1678_ (.CLK(clknet_leaf_1_clk_ref),
    .D(_0276_),
    .SET_B(rst_n),
    .Q(ctrl_k[1]));
 sky130_fd_sc_hd__dfrtp_1 _1679_ (.CLK(clknet_leaf_3_clk_ref),
    .D(_0275_),
    .RESET_B(rst_n),
    .Q(ctrl_k[2]));
 sky130_fd_sc_hd__dfstp_2 _1680_ (.CLK(clknet_leaf_4_clk_ref),
    .D(_0274_),
    .SET_B(rst_n),
    .Q(ctrl_k[3]));
 sky130_fd_sc_hd__dfrtp_1 _1681_ (.CLK(clknet_leaf_14_clk_ref),
    .D(_0208_),
    .RESET_B(rst_n),
    .Q(ctrl_k[4]));
 sky130_fd_sc_hd__dfrtp_1 _1682_ (.CLK(clknet_leaf_32_clk_ref),
    .D(_0273_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [0]));
 sky130_fd_sc_hd__dfrtp_1 _1683_ (.CLK(clknet_leaf_16_clk_ref),
    .D(_0272_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [1]));
 sky130_fd_sc_hd__dfrtp_1 _1684_ (.CLK(clknet_leaf_16_clk_ref),
    .D(_0271_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [2]));
 sky130_fd_sc_hd__dfrtp_1 _1685_ (.CLK(clknet_leaf_22_clk_ref),
    .D(_0269_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [3]));
 sky130_fd_sc_hd__dfrtp_1 _1686_ (.CLK(clknet_leaf_21_clk_ref),
    .D(_0268_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [4]));
 sky130_fd_sc_hd__dfrtp_1 _1687_ (.CLK(clknet_leaf_25_clk_ref),
    .D(_0267_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [5]));
 sky130_fd_sc_hd__dfrtp_1 _1688_ (.CLK(clknet_leaf_22_clk_ref),
    .D(_0266_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [6]));
 sky130_fd_sc_hd__dfrtp_1 _1689_ (.CLK(clknet_leaf_22_clk_ref),
    .D(_0265_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [7]));
 sky130_fd_sc_hd__dfrtp_1 _1690_ (.CLK(clknet_leaf_21_clk_ref),
    .D(_0264_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [8]));
 sky130_fd_sc_hd__dfrtp_1 _1691_ (.CLK(clknet_leaf_26_clk_ref),
    .D(_0263_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [9]));
 sky130_fd_sc_hd__dfrtp_1 _1692_ (.CLK(clknet_leaf_24_clk_ref),
    .D(_0261_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [10]));
 sky130_fd_sc_hd__dfrtp_1 _1693_ (.CLK(clknet_leaf_25_clk_ref),
    .D(_0260_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [11]));
 sky130_fd_sc_hd__dfrtp_1 _1694_ (.CLK(clknet_leaf_32_clk_ref),
    .D(_0259_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [12]));
 sky130_fd_sc_hd__dfrtp_1 _1695_ (.CLK(clknet_leaf_28_clk_ref),
    .D(_0258_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [13]));
 sky130_fd_sc_hd__dfrtp_1 _1696_ (.CLK(clknet_leaf_30_clk_ref),
    .D(_0257_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [14]));
 sky130_fd_sc_hd__dfrtp_1 _1697_ (.CLK(clknet_leaf_29_clk_ref),
    .D(_0256_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [15]));
 sky130_fd_sc_hd__dfrtp_1 _1698_ (.CLK(clknet_leaf_35_clk_ref),
    .D(_0255_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [16]));
 sky130_fd_sc_hd__dfrtp_1 _1699_ (.CLK(clknet_leaf_33_clk_ref),
    .D(_0254_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [17]));
 sky130_fd_sc_hd__dfrtp_1 _1700_ (.CLK(clknet_leaf_35_clk_ref),
    .D(_0253_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [18]));
 sky130_fd_sc_hd__dfrtp_1 _1701_ (.CLK(clknet_leaf_28_clk_ref),
    .D(_0252_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [19]));
 sky130_fd_sc_hd__dfrtp_1 _1702_ (.CLK(clknet_leaf_33_clk_ref),
    .D(_0251_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [20]));
 sky130_fd_sc_hd__dfrtp_1 _1703_ (.CLK(clknet_leaf_33_clk_ref),
    .D(_0250_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [21]));
 sky130_fd_sc_hd__dfrtp_1 _1704_ (.CLK(clknet_leaf_31_clk_ref),
    .D(_0249_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [22]));
 sky130_fd_sc_hd__dfrtp_1 _1705_ (.CLK(clknet_leaf_28_clk_ref),
    .D(_0209_),
    .RESET_B(rst_n),
    .Q(\count_r[0] [23]));
 sky130_fd_sc_hd__dfrtp_1 _1706_ (.CLK(clknet_leaf_1_clk_ref),
    .D(_0210_),
    .RESET_B(rst_n),
    .Q(busy_r));
 sky130_fd_sc_hd__dfrtp_1 _1707_ (.CLK(clknet_leaf_1_clk_ref),
    .D(_0212_),
    .RESET_B(rst_n),
    .Q(done_r));
 sky130_fd_sc_hd__dfrtp_1 _1708_ (.CLK(clknet_leaf_0_clk_ref),
    .D(_0248_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [0]));
 sky130_fd_sc_hd__dfrtp_1 _1709_ (.CLK(clknet_leaf_4_clk_ref),
    .D(_0247_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [1]));
 sky130_fd_sc_hd__dfrtp_1 _1710_ (.CLK(clknet_leaf_7_clk_ref),
    .D(_0246_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [2]));
 sky130_fd_sc_hd__dfrtp_1 _1711_ (.CLK(clknet_leaf_14_clk_ref),
    .D(_0245_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [3]));
 sky130_fd_sc_hd__dfrtp_1 _1712_ (.CLK(clknet_leaf_11_clk_ref),
    .D(_0244_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [4]));
 sky130_fd_sc_hd__dfrtp_1 _1713_ (.CLK(clknet_leaf_2_clk_ref),
    .D(_0243_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [5]));
 sky130_fd_sc_hd__dfrtp_1 _1714_ (.CLK(clknet_leaf_14_clk_ref),
    .D(_0242_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [6]));
 sky130_fd_sc_hd__dfrtp_1 _1715_ (.CLK(clknet_leaf_13_clk_ref),
    .D(_0241_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [7]));
 sky130_fd_sc_hd__dfrtp_1 _1716_ (.CLK(clknet_leaf_12_clk_ref),
    .D(_0240_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [8]));
 sky130_fd_sc_hd__dfrtp_1 _1717_ (.CLK(clknet_leaf_37_clk_ref),
    .D(_0239_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [9]));
 sky130_fd_sc_hd__dfrtp_1 _1718_ (.CLK(clknet_leaf_8_clk_ref),
    .D(_0238_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [10]));
 sky130_fd_sc_hd__dfrtp_1 _1719_ (.CLK(clknet_leaf_11_clk_ref),
    .D(_0237_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [11]));
 sky130_fd_sc_hd__dfrtp_1 _1720_ (.CLK(clknet_leaf_40_clk_ref),
    .D(_0236_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [12]));
 sky130_fd_sc_hd__dfrtp_1 _1721_ (.CLK(clknet_leaf_38_clk_ref),
    .D(_0235_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [13]));
 sky130_fd_sc_hd__dfrtp_1 _1722_ (.CLK(clknet_leaf_37_clk_ref),
    .D(_0234_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [14]));
 sky130_fd_sc_hd__dfrtp_1 _1723_ (.CLK(clknet_leaf_8_clk_ref),
    .D(_0233_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [15]));
 sky130_fd_sc_hd__dfrtp_1 _1724_ (.CLK(clknet_leaf_36_clk_ref),
    .D(_0232_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [16]));
 sky130_fd_sc_hd__dfrtp_1 _1725_ (.CLK(clknet_leaf_0_clk_ref),
    .D(_0231_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [17]));
 sky130_fd_sc_hd__dfrtp_1 _1726_ (.CLK(clknet_leaf_10_clk_ref),
    .D(_0230_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [18]));
 sky130_fd_sc_hd__dfrtp_1 _1727_ (.CLK(clknet_leaf_9_clk_ref),
    .D(_0229_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [19]));
 sky130_fd_sc_hd__dfrtp_1 _1728_ (.CLK(clknet_leaf_39_clk_ref),
    .D(_0228_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [20]));
 sky130_fd_sc_hd__dfrtp_1 _1729_ (.CLK(clknet_leaf_33_clk_ref),
    .D(_0227_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [21]));
 sky130_fd_sc_hd__dfrtp_1 _1730_ (.CLK(clknet_leaf_8_clk_ref),
    .D(_0226_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [22]));
 sky130_fd_sc_hd__dfrtp_1 _1731_ (.CLK(clknet_leaf_37_clk_ref),
    .D(_0213_),
    .RESET_B(rst_n),
    .Q(\cal_r[4] [23]));
 sky130_fd_sc_hd__dfrtp_1 _1732_ (.CLK(clknet_leaf_0_clk_ref),
    .D(_0225_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [0]));
 sky130_fd_sc_hd__dfrtp_1 _1733_ (.CLK(clknet_leaf_6_clk_ref),
    .D(_0224_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [1]));
 sky130_fd_sc_hd__dfrtp_1 _1734_ (.CLK(clknet_leaf_7_clk_ref),
    .D(_0223_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [2]));
 sky130_fd_sc_hd__dfrtp_1 _1735_ (.CLK(clknet_leaf_4_clk_ref),
    .D(_0222_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [3]));
 sky130_fd_sc_hd__dfrtp_1 _1736_ (.CLK(clknet_leaf_11_clk_ref),
    .D(_0221_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [4]));
 sky130_fd_sc_hd__dfrtp_1 _1737_ (.CLK(clknet_leaf_2_clk_ref),
    .D(_0218_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [5]));
 sky130_fd_sc_hd__dfrtp_1 _1738_ (.CLK(clknet_leaf_13_clk_ref),
    .D(_0217_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [6]));
 sky130_fd_sc_hd__dfrtp_1 _1739_ (.CLK(clknet_leaf_13_clk_ref),
    .D(_0216_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [7]));
 sky130_fd_sc_hd__dfrtp_1 _1740_ (.CLK(clknet_leaf_12_clk_ref),
    .D(_0211_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [8]));
 sky130_fd_sc_hd__dfrtp_1 _1741_ (.CLK(clknet_leaf_36_clk_ref),
    .D(_0202_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [9]));
 sky130_fd_sc_hd__dfrtp_1 _1742_ (.CLK(clknet_leaf_9_clk_ref),
    .D(_0199_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [10]));
 sky130_fd_sc_hd__dfrtp_1 _1743_ (.CLK(clknet_leaf_10_clk_ref),
    .D(_0198_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [11]));
 sky130_fd_sc_hd__dfrtp_1 _1744_ (.CLK(clknet_leaf_40_clk_ref),
    .D(_0197_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [12]));
 sky130_fd_sc_hd__dfrtp_1 _1745_ (.CLK(clknet_leaf_38_clk_ref),
    .D(_0196_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [13]));
 sky130_fd_sc_hd__dfrtp_1 _1746_ (.CLK(clknet_leaf_36_clk_ref),
    .D(_0195_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [14]));
 sky130_fd_sc_hd__dfrtp_1 _1747_ (.CLK(clknet_leaf_6_clk_ref),
    .D(_0194_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [15]));
 sky130_fd_sc_hd__dfrtp_1 _1748_ (.CLK(clknet_leaf_39_clk_ref),
    .D(_0193_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [16]));
 sky130_fd_sc_hd__dfrtp_1 _1749_ (.CLK(clknet_leaf_5_clk_ref),
    .D(_0192_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [17]));
 sky130_fd_sc_hd__dfrtp_1 _1750_ (.CLK(clknet_leaf_9_clk_ref),
    .D(_0191_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [18]));
 sky130_fd_sc_hd__dfrtp_1 _1751_ (.CLK(clknet_leaf_9_clk_ref),
    .D(_0190_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [19]));
 sky130_fd_sc_hd__dfrtp_1 _1752_ (.CLK(clknet_leaf_39_clk_ref),
    .D(_0189_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [20]));
 sky130_fd_sc_hd__dfrtp_1 _1753_ (.CLK(clknet_leaf_39_clk_ref),
    .D(_0188_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [21]));
 sky130_fd_sc_hd__dfrtp_1 _1754_ (.CLK(clknet_leaf_8_clk_ref),
    .D(_0187_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [22]));
 sky130_fd_sc_hd__dfrtp_1 _1755_ (.CLK(clknet_leaf_38_clk_ref),
    .D(_0214_),
    .RESET_B(rst_n),
    .Q(\cal_r[1] [23]));
 sky130_fd_sc_hd__dfrtp_1 _1756_ (.CLK(clknet_leaf_2_clk_ref),
    .D(_0215_),
    .RESET_B(rst_n),
    .Q(ovf_r));
 sky130_fd_sc_hd__dfrtp_1 _1757_ (.CLK(clknet_leaf_23_clk_ref),
    .D(_0186_),
    .RESET_B(rst_n),
    .Q(gate_cnt[0]));
 sky130_fd_sc_hd__dfrtp_1 _1758_ (.CLK(clknet_leaf_17_clk_ref),
    .D(_0185_),
    .RESET_B(rst_n),
    .Q(gate_cnt[1]));
 sky130_fd_sc_hd__dfrtp_1 _1759_ (.CLK(clknet_leaf_20_clk_ref),
    .D(_0184_),
    .RESET_B(rst_n),
    .Q(gate_cnt[2]));
 sky130_fd_sc_hd__dfrtp_1 _1760_ (.CLK(clknet_leaf_20_clk_ref),
    .D(_0183_),
    .RESET_B(rst_n),
    .Q(gate_cnt[3]));
 sky130_fd_sc_hd__dfrtp_1 _1761_ (.CLK(clknet_leaf_19_clk_ref),
    .D(_0182_),
    .RESET_B(rst_n),
    .Q(gate_cnt[4]));
 sky130_fd_sc_hd__dfrtp_1 _1762_ (.CLK(clknet_leaf_20_clk_ref),
    .D(_0181_),
    .RESET_B(rst_n),
    .Q(gate_cnt[5]));
 sky130_fd_sc_hd__dfrtp_1 _1763_ (.CLK(clknet_leaf_18_clk_ref),
    .D(_0180_),
    .RESET_B(rst_n),
    .Q(gate_cnt[6]));
 sky130_fd_sc_hd__dfrtp_1 _1764_ (.CLK(clknet_leaf_18_clk_ref),
    .D(_0179_),
    .RESET_B(rst_n),
    .Q(gate_cnt[7]));
 sky130_fd_sc_hd__dfrtp_1 _1765_ (.CLK(clknet_leaf_18_clk_ref),
    .D(_0178_),
    .RESET_B(rst_n),
    .Q(gate_cnt[8]));
 sky130_fd_sc_hd__dfrtp_1 _1766_ (.CLK(clknet_leaf_20_clk_ref),
    .D(_0177_),
    .RESET_B(rst_n),
    .Q(gate_cnt[9]));
 sky130_fd_sc_hd__dfrtp_1 _1767_ (.CLK(clknet_leaf_19_clk_ref),
    .D(_0176_),
    .RESET_B(rst_n),
    .Q(gate_cnt[10]));
 sky130_fd_sc_hd__dfrtp_1 _1768_ (.CLK(clknet_leaf_19_clk_ref),
    .D(_0175_),
    .RESET_B(rst_n),
    .Q(gate_cnt[11]));
 sky130_fd_sc_hd__dfrtp_1 _1769_ (.CLK(clknet_leaf_19_clk_ref),
    .D(_0174_),
    .RESET_B(rst_n),
    .Q(gate_cnt[12]));
 sky130_fd_sc_hd__dfrtp_1 _1770_ (.CLK(clknet_leaf_19_clk_ref),
    .D(_0173_),
    .RESET_B(rst_n),
    .Q(gate_cnt[13]));
 sky130_fd_sc_hd__dfrtp_1 _1771_ (.CLK(clknet_leaf_19_clk_ref),
    .D(_0172_),
    .RESET_B(rst_n),
    .Q(gate_cnt[14]));
 sky130_fd_sc_hd__dfrtp_1 _1772_ (.CLK(clknet_leaf_19_clk_ref),
    .D(_0171_),
    .RESET_B(rst_n),
    .Q(gate_cnt[15]));
 sky130_fd_sc_hd__dfrtp_1 _1773_ (.CLK(clknet_leaf_18_clk_ref),
    .D(_0170_),
    .RESET_B(rst_n),
    .Q(gate_cnt[16]));
 sky130_fd_sc_hd__dfrtp_1 _1774_ (.CLK(clknet_leaf_18_clk_ref),
    .D(_0169_),
    .RESET_B(rst_n),
    .Q(gate_cnt[17]));
 sky130_fd_sc_hd__dfrtp_1 _1775_ (.CLK(clknet_leaf_17_clk_ref),
    .D(_0168_),
    .RESET_B(rst_n),
    .Q(gate_cnt[18]));
 sky130_fd_sc_hd__dfrtp_1 _1776_ (.CLK(clknet_leaf_18_clk_ref),
    .D(_0167_),
    .RESET_B(rst_n),
    .Q(gate_cnt[19]));
 sky130_fd_sc_hd__dfrtp_1 _1777_ (.CLK(clknet_leaf_17_clk_ref),
    .D(_0166_),
    .RESET_B(rst_n),
    .Q(gate_cnt[20]));
 sky130_fd_sc_hd__dfrtp_1 _1778_ (.CLK(clknet_leaf_17_clk_ref),
    .D(_0165_),
    .RESET_B(rst_n),
    .Q(gate_cnt[21]));
 sky130_fd_sc_hd__dfrtp_1 _1779_ (.CLK(clknet_leaf_12_clk_ref),
    .D(_0164_),
    .RESET_B(rst_n),
    .Q(gate_cnt[22]));
 sky130_fd_sc_hd__dfrtp_1 _1780_ (.CLK(clknet_leaf_12_clk_ref),
    .D(_0163_),
    .RESET_B(rst_n),
    .Q(gate_cnt[23]));
 sky130_fd_sc_hd__dfrtp_1 _1781_ (.CLK(clknet_leaf_12_clk_ref),
    .D(_0162_),
    .RESET_B(rst_n),
    .Q(gate_cnt[24]));
 sky130_fd_sc_hd__dfrtp_1 _1782_ (.CLK(clknet_leaf_13_clk_ref),
    .D(_0161_),
    .RESET_B(rst_n),
    .Q(gate_cnt[25]));
 sky130_fd_sc_hd__dfrtp_1 _1783_ (.CLK(clknet_leaf_13_clk_ref),
    .D(_0160_),
    .RESET_B(rst_n),
    .Q(gate_cnt[26]));
 sky130_fd_sc_hd__dfrtp_1 _1784_ (.CLK(clknet_leaf_13_clk_ref),
    .D(_0159_),
    .RESET_B(rst_n),
    .Q(gate_cnt[27]));
 sky130_fd_sc_hd__dfrtp_1 _1785_ (.CLK(clknet_leaf_23_clk_ref),
    .D(_0158_),
    .RESET_B(rst_n),
    .Q(gate_cnt[28]));
 sky130_fd_sc_hd__dfrtp_1 _1786_ (.CLK(clknet_leaf_17_clk_ref),
    .D(_0157_),
    .RESET_B(rst_n),
    .Q(gate_cnt[29]));
 sky130_fd_sc_hd__dfrtp_1 _1787_ (.CLK(clknet_leaf_16_clk_ref),
    .D(_0156_),
    .RESET_B(rst_n),
    .Q(gate_cnt[30]));
 sky130_fd_sc_hd__dfrtp_1 _1788_ (.CLK(clknet_leaf_17_clk_ref),
    .D(_0219_),
    .RESET_B(rst_n),
    .Q(gate_cnt[31]));
 sky130_fd_sc_hd__dfrtp_1 _1789_ (.CLK(clknet_leaf_0_clk_ref),
    .D(_0155_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [0]));
 sky130_fd_sc_hd__dfrtp_1 _1790_ (.CLK(clknet_leaf_5_clk_ref),
    .D(_0154_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [1]));
 sky130_fd_sc_hd__dfrtp_1 _1791_ (.CLK(clknet_leaf_7_clk_ref),
    .D(_0153_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [2]));
 sky130_fd_sc_hd__dfrtp_1 _1792_ (.CLK(clknet_leaf_14_clk_ref),
    .D(_0152_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [3]));
 sky130_fd_sc_hd__dfrtp_1 _1793_ (.CLK(clknet_leaf_7_clk_ref),
    .D(_0151_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [4]));
 sky130_fd_sc_hd__dfrtp_1 _1794_ (.CLK(clknet_leaf_2_clk_ref),
    .D(_0150_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [5]));
 sky130_fd_sc_hd__dfrtp_1 _1795_ (.CLK(clknet_leaf_14_clk_ref),
    .D(_0149_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [6]));
 sky130_fd_sc_hd__dfrtp_1 _1796_ (.CLK(clknet_leaf_11_clk_ref),
    .D(_0148_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [7]));
 sky130_fd_sc_hd__dfrtp_1 _1797_ (.CLK(clknet_leaf_12_clk_ref),
    .D(_0147_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [8]));
 sky130_fd_sc_hd__dfrtp_1 _1798_ (.CLK(clknet_leaf_35_clk_ref),
    .D(_0146_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [9]));
 sky130_fd_sc_hd__dfrtp_1 _1799_ (.CLK(clknet_leaf_7_clk_ref),
    .D(_0145_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [10]));
 sky130_fd_sc_hd__dfrtp_1 _1800_ (.CLK(clknet_leaf_10_clk_ref),
    .D(_0144_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [11]));
 sky130_fd_sc_hd__dfrtp_1 _1801_ (.CLK(clknet_leaf_40_clk_ref),
    .D(_0143_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [12]));
 sky130_fd_sc_hd__dfrtp_1 _1802_ (.CLK(clknet_leaf_38_clk_ref),
    .D(_0142_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [13]));
 sky130_fd_sc_hd__dfrtp_1 _1803_ (.CLK(clknet_leaf_37_clk_ref),
    .D(_0141_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [14]));
 sky130_fd_sc_hd__dfrtp_1 _1804_ (.CLK(clknet_leaf_6_clk_ref),
    .D(_0140_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [15]));
 sky130_fd_sc_hd__dfrtp_1 _1805_ (.CLK(clknet_leaf_36_clk_ref),
    .D(_0139_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [16]));
 sky130_fd_sc_hd__dfrtp_1 _1806_ (.CLK(clknet_leaf_5_clk_ref),
    .D(_0138_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [17]));
 sky130_fd_sc_hd__dfrtp_1 _1807_ (.CLK(clknet_leaf_10_clk_ref),
    .D(_0137_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [18]));
 sky130_fd_sc_hd__dfrtp_1 _1808_ (.CLK(clknet_leaf_9_clk_ref),
    .D(_0136_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [19]));
 sky130_fd_sc_hd__dfrtp_1 _1809_ (.CLK(clknet_leaf_39_clk_ref),
    .D(_0135_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [20]));
 sky130_fd_sc_hd__dfrtp_1 _1810_ (.CLK(clknet_leaf_1_clk_ref),
    .D(_0134_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [21]));
 sky130_fd_sc_hd__dfrtp_1 _1811_ (.CLK(clknet_leaf_9_clk_ref),
    .D(_0133_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [22]));
 sky130_fd_sc_hd__dfrtp_1 _1812_ (.CLK(clknet_leaf_37_clk_ref),
    .D(_0220_),
    .RESET_B(rst_n),
    .Q(\cal_r[3] [23]));
 sky130_fd_sc_hd__dfrtp_1 _1813_ (.CLK(clknet_leaf_3_clk_ref),
    .D(_0132_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [0]));
 sky130_fd_sc_hd__dfrtp_1 _1814_ (.CLK(clknet_leaf_14_clk_ref),
    .D(_0131_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [1]));
 sky130_fd_sc_hd__dfrtp_1 _1815_ (.CLK(clknet_leaf_16_clk_ref),
    .D(_0130_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [2]));
 sky130_fd_sc_hd__dfrtp_1 _1816_ (.CLK(clknet_leaf_21_clk_ref),
    .D(_0129_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [3]));
 sky130_fd_sc_hd__dfrtp_1 _1817_ (.CLK(clknet_leaf_21_clk_ref),
    .D(_0128_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [4]));
 sky130_fd_sc_hd__dfrtp_1 _1818_ (.CLK(clknet_leaf_25_clk_ref),
    .D(_0127_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [5]));
 sky130_fd_sc_hd__dfrtp_1 _1819_ (.CLK(clknet_leaf_23_clk_ref),
    .D(_0126_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [6]));
 sky130_fd_sc_hd__dfrtp_1 _1820_ (.CLK(clknet_leaf_23_clk_ref),
    .D(_0125_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [7]));
 sky130_fd_sc_hd__dfrtp_1 _1821_ (.CLK(clknet_leaf_20_clk_ref),
    .D(_0124_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [8]));
 sky130_fd_sc_hd__dfrtp_1 _1822_ (.CLK(clknet_leaf_26_clk_ref),
    .D(_0123_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [9]));
 sky130_fd_sc_hd__dfrtp_1 _1823_ (.CLK(clknet_leaf_15_clk_ref),
    .D(_0122_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [10]));
 sky130_fd_sc_hd__dfrtp_1 _1824_ (.CLK(clknet_leaf_27_clk_ref),
    .D(_0121_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [11]));
 sky130_fd_sc_hd__dfrtp_1 _1825_ (.CLK(clknet_leaf_24_clk_ref),
    .D(_0120_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [12]));
 sky130_fd_sc_hd__dfrtp_1 _1826_ (.CLK(clknet_leaf_27_clk_ref),
    .D(_0119_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [13]));
 sky130_fd_sc_hd__dfrtp_1 _1827_ (.CLK(clknet_leaf_30_clk_ref),
    .D(_0118_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [14]));
 sky130_fd_sc_hd__dfrtp_1 _1828_ (.CLK(clknet_leaf_29_clk_ref),
    .D(_0117_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [15]));
 sky130_fd_sc_hd__dfrtp_1 _1829_ (.CLK(clknet_leaf_35_clk_ref),
    .D(_0116_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [16]));
 sky130_fd_sc_hd__dfrtp_1 _1830_ (.CLK(clknet_leaf_32_clk_ref),
    .D(_0115_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [17]));
 sky130_fd_sc_hd__dfrtp_1 _1831_ (.CLK(clknet_leaf_35_clk_ref),
    .D(_0114_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [18]));
 sky130_fd_sc_hd__dfrtp_1 _1832_ (.CLK(clknet_leaf_29_clk_ref),
    .D(_0113_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [19]));
 sky130_fd_sc_hd__dfrtp_1 _1833_ (.CLK(clknet_leaf_34_clk_ref),
    .D(_0112_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [20]));
 sky130_fd_sc_hd__dfrtp_1 _1834_ (.CLK(clknet_leaf_34_clk_ref),
    .D(_0111_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [21]));
 sky130_fd_sc_hd__dfrtp_1 _1835_ (.CLK(clknet_leaf_31_clk_ref),
    .D(_0110_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [22]));
 sky130_fd_sc_hd__dfrtp_1 _1836_ (.CLK(clknet_leaf_28_clk_ref),
    .D(_0262_),
    .RESET_B(rst_n),
    .Q(\count_r[4] [23]));
 sky130_fd_sc_hd__dfrtp_1 _1837_ (.CLK(clknet_leaf_0_clk_ref),
    .D(_0107_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [0]));
 sky130_fd_sc_hd__dfrtp_1 _1838_ (.CLK(clknet_leaf_5_clk_ref),
    .D(_0106_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [1]));
 sky130_fd_sc_hd__dfrtp_1 _1839_ (.CLK(clknet_leaf_7_clk_ref),
    .D(_0105_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [2]));
 sky130_fd_sc_hd__dfrtp_1 _1840_ (.CLK(clknet_leaf_14_clk_ref),
    .D(_0104_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [3]));
 sky130_fd_sc_hd__dfrtp_1 _1841_ (.CLK(clknet_leaf_10_clk_ref),
    .D(_0103_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [4]));
 sky130_fd_sc_hd__dfrtp_1 _1842_ (.CLK(clknet_leaf_2_clk_ref),
    .D(_0102_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [5]));
 sky130_fd_sc_hd__dfrtp_1 _1843_ (.CLK(clknet_leaf_4_clk_ref),
    .D(_0101_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [6]));
 sky130_fd_sc_hd__dfrtp_1 _1844_ (.CLK(clknet_leaf_11_clk_ref),
    .D(_0100_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [7]));
 sky130_fd_sc_hd__dfrtp_1 _1845_ (.CLK(clknet_leaf_12_clk_ref),
    .D(_0099_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [8]));
 sky130_fd_sc_hd__dfrtp_1 _1846_ (.CLK(clknet_leaf_36_clk_ref),
    .D(_0098_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [9]));
 sky130_fd_sc_hd__dfrtp_1 _1847_ (.CLK(clknet_leaf_6_clk_ref),
    .D(_0097_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [10]));
 sky130_fd_sc_hd__dfrtp_1 _1848_ (.CLK(clknet_leaf_10_clk_ref),
    .D(_0096_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [11]));
 sky130_fd_sc_hd__dfrtp_1 _1849_ (.CLK(clknet_leaf_40_clk_ref),
    .D(_0095_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [12]));
 sky130_fd_sc_hd__dfrtp_1 _1850_ (.CLK(clknet_leaf_38_clk_ref),
    .D(_0094_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [13]));
 sky130_fd_sc_hd__dfrtp_1 _1851_ (.CLK(clknet_leaf_37_clk_ref),
    .D(_0093_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [14]));
 sky130_fd_sc_hd__dfrtp_1 _1852_ (.CLK(clknet_leaf_6_clk_ref),
    .D(_0092_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [15]));
 sky130_fd_sc_hd__dfrtp_1 _1853_ (.CLK(clknet_leaf_36_clk_ref),
    .D(_0091_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [16]));
 sky130_fd_sc_hd__dfrtp_1 _1854_ (.CLK(clknet_leaf_5_clk_ref),
    .D(_0090_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [17]));
 sky130_fd_sc_hd__dfrtp_1 _1855_ (.CLK(clknet_leaf_9_clk_ref),
    .D(_0089_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [18]));
 sky130_fd_sc_hd__dfrtp_1 _1856_ (.CLK(clknet_leaf_8_clk_ref),
    .D(_0088_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [19]));
 sky130_fd_sc_hd__dfrtp_1 _1857_ (.CLK(clknet_leaf_39_clk_ref),
    .D(_0087_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [20]));
 sky130_fd_sc_hd__dfrtp_1 _1858_ (.CLK(clknet_leaf_2_clk_ref),
    .D(_0109_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [21]));
 sky130_fd_sc_hd__dfrtp_1 _1859_ (.CLK(clknet_leaf_8_clk_ref),
    .D(_0108_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [22]));
 sky130_fd_sc_hd__dfrtp_1 _1860_ (.CLK(clknet_leaf_38_clk_ref),
    .D(_0270_),
    .RESET_B(rst_n),
    .Q(\cal_r[2] [23]));
 sky130_fd_sc_hd__dfrtp_1 _1861_ (.CLK(clknet_leaf_16_clk_ref),
    .D(_0000_),
    .RESET_B(rst_n),
    .Q(gate_en));
 sky130_fd_sc_hd__dfrtp_1 _1862_ (.CLK(clknet_leaf_2_clk_ref),
    .D(tog_o),
    .RESET_B(rst_n),
    .Q(tog_s1));
 sky130_fd_sc_hd__dfrtp_1 _1863_ (.CLK(clknet_leaf_1_clk_ref),
    .D(tog_s1),
    .RESET_B(rst_n),
    .Q(tog_s2));
 sky130_fd_sc_hd__dfrtp_1 _1864_ (.CLK(clknet_leaf_1_clk_ref),
    .D(tog_s2),
    .RESET_B(rst_n),
    .Q(tog_s3));
 sky130_fd_sc_hd__conb_1 _1865_ (.LO(_0772_));
 sky130_fd_sc_hd__buf_4 clkbuf_0_clk_ref (.A(clk_ref),
    .X(clknet_0_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_2_0__f_clk_ref (.A(clknet_0_clk_ref),
    .X(clknet_2_0__leaf_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_2_1__f_clk_ref (.A(clknet_0_clk_ref),
    .X(clknet_2_1__leaf_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_2_2__f_clk_ref (.A(clknet_0_clk_ref),
    .X(clknet_2_2__leaf_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_2_3__f_clk_ref (.A(clknet_0_clk_ref),
    .X(clknet_2_3__leaf_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_0_clk_ref (.A(clknet_2_0__leaf_clk_ref),
    .X(clknet_leaf_0_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_10_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_10_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_11_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_11_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_12_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_12_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_13_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_13_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_14_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_14_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_15_clk_ref (.A(clknet_2_3__leaf_clk_ref),
    .X(clknet_leaf_15_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_16_clk_ref (.A(clknet_2_3__leaf_clk_ref),
    .X(clknet_leaf_16_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_17_clk_ref (.A(clknet_2_3__leaf_clk_ref),
    .X(clknet_leaf_17_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_18_clk_ref (.A(clknet_2_3__leaf_clk_ref),
    .X(clknet_leaf_18_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_19_clk_ref (.A(clknet_2_3__leaf_clk_ref),
    .X(clknet_leaf_19_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_1_clk_ref (.A(clknet_2_0__leaf_clk_ref),
    .X(clknet_leaf_1_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_20_clk_ref (.A(clknet_2_3__leaf_clk_ref),
    .X(clknet_leaf_20_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_21_clk_ref (.A(clknet_2_3__leaf_clk_ref),
    .X(clknet_leaf_21_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_22_clk_ref (.A(clknet_2_3__leaf_clk_ref),
    .X(clknet_leaf_22_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_23_clk_ref (.A(clknet_2_3__leaf_clk_ref),
    .X(clknet_leaf_23_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_24_clk_ref (.A(clknet_2_3__leaf_clk_ref),
    .X(clknet_leaf_24_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_25_clk_ref (.A(clknet_2_1__leaf_clk_ref),
    .X(clknet_leaf_25_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_26_clk_ref (.A(clknet_2_1__leaf_clk_ref),
    .X(clknet_leaf_26_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_27_clk_ref (.A(clknet_2_1__leaf_clk_ref),
    .X(clknet_leaf_27_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_28_clk_ref (.A(clknet_2_1__leaf_clk_ref),
    .X(clknet_leaf_28_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_29_clk_ref (.A(clknet_2_1__leaf_clk_ref),
    .X(clknet_leaf_29_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_2_clk_ref (.A(clknet_2_0__leaf_clk_ref),
    .X(clknet_leaf_2_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_30_clk_ref (.A(clknet_2_1__leaf_clk_ref),
    .X(clknet_leaf_30_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_31_clk_ref (.A(clknet_2_1__leaf_clk_ref),
    .X(clknet_leaf_31_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_32_clk_ref (.A(clknet_2_1__leaf_clk_ref),
    .X(clknet_leaf_32_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_33_clk_ref (.A(clknet_2_0__leaf_clk_ref),
    .X(clknet_leaf_33_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_34_clk_ref (.A(clknet_2_1__leaf_clk_ref),
    .X(clknet_leaf_34_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_35_clk_ref (.A(clknet_2_0__leaf_clk_ref),
    .X(clknet_leaf_35_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_36_clk_ref (.A(clknet_2_0__leaf_clk_ref),
    .X(clknet_leaf_36_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_37_clk_ref (.A(clknet_2_0__leaf_clk_ref),
    .X(clknet_leaf_37_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_38_clk_ref (.A(clknet_2_0__leaf_clk_ref),
    .X(clknet_leaf_38_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_39_clk_ref (.A(clknet_2_0__leaf_clk_ref),
    .X(clknet_leaf_39_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_3_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_3_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_40_clk_ref (.A(clknet_2_0__leaf_clk_ref),
    .X(clknet_leaf_40_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_4_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_4_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_5_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_5_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_6_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_6_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_7_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_7_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_8_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_8_clk_ref));
 sky130_fd_sc_hd__buf_4 clkbuf_leaf_9_clk_ref (.A(clknet_2_2__leaf_clk_ref),
    .X(clknet_leaf_9_clk_ref));
 sky130_fd_sc_hd__clkinvlp_2 clkload0 (.A(clknet_2_0__leaf_clk_ref));
 sky130_fd_sc_hd__bufinv_16 clkload1 (.A(clknet_2_1__leaf_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload10 (.A(clknet_leaf_29_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload11 (.A(clknet_leaf_31_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload12 (.A(clknet_leaf_32_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload13 (.A(clknet_leaf_34_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload14 (.A(clknet_leaf_3_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload15 (.A(clknet_leaf_4_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload16 (.A(clknet_leaf_5_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload17 (.A(clknet_leaf_6_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload18 (.A(clknet_leaf_7_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload19 (.A(clknet_leaf_9_clk_ref));
 sky130_fd_sc_hd__clkinvlp_2 clkload2 (.A(clknet_2_3__leaf_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload20 (.A(clknet_leaf_10_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload21 (.A(clknet_leaf_11_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload22 (.A(clknet_leaf_12_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload23 (.A(clknet_leaf_13_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload24 (.A(clknet_leaf_14_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload25 (.A(clknet_leaf_15_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload26 (.A(clknet_leaf_17_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload27 (.A(clknet_leaf_18_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload28 (.A(clknet_leaf_19_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload29 (.A(clknet_leaf_20_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload3 (.A(clknet_leaf_0_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload30 (.A(clknet_leaf_21_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload31 (.A(clknet_leaf_22_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload32 (.A(clknet_leaf_23_clk_ref));
 sky130_fd_sc_hd__bufinv_16 clkload33 (.A(clknet_leaf_24_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload4 (.A(clknet_leaf_1_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload5 (.A(clknet_leaf_37_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload6 (.A(clknet_leaf_39_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload7 (.A(clknet_leaf_40_clk_ref));
 sky130_fd_sc_hd__inv_1 clkload8 (.A(clknet_leaf_27_clk_ref));
 sky130_fd_sc_hd__clkinv_1 clkload9 (.A(clknet_leaf_28_clk_ref));
 sky130_fd_sc_hd__buf_4 place10 (.A(_0450_),
    .X(net10));
 sky130_fd_sc_hd__buf_4 place11 (.A(_0359_),
    .X(net11));
 sky130_fd_sc_hd__buf_4 place12 (.A(_0353_),
    .X(net12));
 sky130_fd_sc_hd__buf_4 place13 (.A(_0315_),
    .X(net13));
 sky130_fd_sc_hd__buf_4 place14 (.A(_0485_),
    .X(net14));
 sky130_fd_sc_hd__buf_4 place15 (.A(_0485_),
    .X(net15));
 sky130_fd_sc_hd__buf_4 place16 (.A(_0483_),
    .X(net16));
 sky130_fd_sc_hd__buf_4 place17 (.A(_0476_),
    .X(net17));
 sky130_fd_sc_hd__buf_4 place18 (.A(_0470_),
    .X(net18));
 sky130_fd_sc_hd__buf_4 place19 (.A(_0500_),
    .X(net19));
 sky130_fd_sc_hd__buf_4 place20 (.A(_0493_),
    .X(net20));
 sky130_fd_sc_hd__buf_4 place21 (.A(_0472_),
    .X(net21));
 sky130_fd_sc_hd__buf_4 place22 (.A(_0472_),
    .X(net22));
 sky130_fd_sc_hd__and3_1 \u_cnt/_107_  (.A(cnt_o[1]),
    .B(cnt_o[0]),
    .C(cnt_o[2]),
    .X(\u_cnt/_068_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_108_  (.A(cnt_o[11]),
    .Y(\u_cnt/_069_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_109_  (.A(cnt_o[12]),
    .Y(\u_cnt/_070_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_110_  (.A(cnt_o[6]),
    .Y(\u_cnt/_071_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_111_  (.A(cnt_o[7]),
    .Y(\u_cnt/_072_ ));
 sky130_fd_sc_hd__nand3_2 \u_cnt/_112_  (.A(cnt_o[1]),
    .B(cnt_o[0]),
    .C(cnt_o[2]),
    .Y(\u_cnt/_073_ ));
 sky130_fd_sc_hd__nand3_1 \u_cnt/_113_  (.A(cnt_o[3]),
    .B(cnt_o[4]),
    .C(cnt_o[5]),
    .Y(\u_cnt/_074_ ));
 sky130_fd_sc_hd__nor4_4 \u_cnt/_114_  (.A(\u_cnt/_071_ ),
    .B(\u_cnt/_072_ ),
    .C(\u_cnt/_073_ ),
    .D(\u_cnt/_074_ ),
    .Y(\u_cnt/_075_ ));
 sky130_fd_sc_hd__nand4_2 \u_cnt/_115_  (.A(cnt_o[8]),
    .B(cnt_o[9]),
    .C(cnt_o[10]),
    .D(\u_cnt/_075_ ),
    .Y(\u_cnt/_076_ ));
 sky130_fd_sc_hd__nand4_1 \u_cnt/_116_  (.A(cnt_o[13]),
    .B(cnt_o[14]),
    .C(cnt_o[15]),
    .D(cnt_o[16]),
    .Y(\u_cnt/_077_ ));
 sky130_fd_sc_hd__nor4_4 \u_cnt/_117_  (.A(\u_cnt/_069_ ),
    .B(\u_cnt/_070_ ),
    .C(\u_cnt/_076_ ),
    .D(\u_cnt/_077_ ),
    .Y(\u_cnt/_078_ ));
 sky130_fd_sc_hd__and4_4 \u_cnt/_118_  (.A(cnt_o[17]),
    .B(cnt_o[18]),
    .C(cnt_o[19]),
    .D(\u_cnt/_078_ ),
    .X(\u_cnt/_079_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_119_  (.A(cnt_o[21]),
    .Y(\u_cnt/_080_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_120_  (.A(cnt_o[22]),
    .Y(\u_cnt/_081_ ));
 sky130_fd_sc_hd__nor2_1 \u_cnt/_121_  (.A(\u_cnt/_080_ ),
    .B(\u_cnt/_081_ ),
    .Y(\u_cnt/_082_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_122_  (.A(\u_cnt/gate_s2 ),
    .Y(\u_cnt/_083_ ));
 sky130_fd_sc_hd__a41oi_2 \u_cnt/_123_  (.A1(cnt_o[20]),
    .A2(cnt_o[23]),
    .A3(\u_cnt/_079_ ),
    .A4(\u_cnt/_082_ ),
    .B1(\u_cnt/_083_ ),
    .Y(\u_cnt/_084_ ));
 sky130_fd_sc_hd__and3_4 \u_cnt/_125_  (.A(cnt_o[3]),
    .B(\u_cnt/_068_ ),
    .C(\u_cnt/_084_ ),
    .X(\u_cnt/_086_ ));
 sky130_fd_sc_hd__nor2_1 \u_cnt/_127_  (.A(\u_cnt/running ),
    .B(\u_cnt/_083_ ),
    .Y(\u_cnt/_088_ ));
 sky130_fd_sc_hd__a41oi_2 \u_cnt/_129_  (.A1(cnt_o[3]),
    .A2(cnt_o[4]),
    .A3(\u_cnt/_068_ ),
    .A4(\u_cnt/_084_ ),
    .B1(\u_cnt/_088_ ),
    .Y(\u_cnt/_090_ ));
 sky130_fd_sc_hd__o21a_1 \u_cnt/_130_  (.A1(cnt_o[4]),
    .A2(\u_cnt/_086_ ),
    .B1(\u_cnt/_090_ ),
    .X(\u_cnt/_000_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_133_  (.A1(\u_cnt/_068_ ),
    .A2(\u_cnt/_084_ ),
    .B1(cnt_o[3]),
    .Y(\u_cnt/_093_ ));
 sky130_fd_sc_hd__nor3_2 \u_cnt/_134_  (.A(\u_cnt/_088_ ),
    .B(\u_cnt/_086_ ),
    .C(\u_cnt/_093_ ),
    .Y(\u_cnt/_001_ ));
 sky130_fd_sc_hd__a31oi_1 \u_cnt/_135_  (.A1(cnt_o[1]),
    .A2(cnt_o[0]),
    .A3(\u_cnt/_084_ ),
    .B1(cnt_o[2]),
    .Y(\u_cnt/_094_ ));
 sky130_fd_sc_hd__a211oi_1 \u_cnt/_136_  (.A1(\u_cnt/_068_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_094_ ),
    .C1(\u_cnt/_088_ ),
    .Y(\u_cnt/_002_ ));
 sky130_fd_sc_hd__nand2b_1 \u_cnt/_137_  (.A_N(\u_cnt/running ),
    .B(\u_cnt/gate_s2 ),
    .Y(\u_cnt/_095_ ));
 sky130_fd_sc_hd__a41o_1 \u_cnt/_138_  (.A1(cnt_o[20]),
    .A2(cnt_o[23]),
    .A3(\u_cnt/_079_ ),
    .A4(\u_cnt/_082_ ),
    .B1(\u_cnt/_083_ ),
    .X(\u_cnt/_096_ ));
 sky130_fd_sc_hd__a21boi_0 \u_cnt/_139_  (.A1(\u_cnt/_095_ ),
    .A2(\u_cnt/_096_ ),
    .B1_N(cnt_o[0]),
    .Y(\u_cnt/_097_ ));
 sky130_fd_sc_hd__a31oi_1 \u_cnt/_141_  (.A1(cnt_o[1]),
    .A2(cnt_o[0]),
    .A3(\u_cnt/_084_ ),
    .B1(\u_cnt/_088_ ),
    .Y(\u_cnt/_099_ ));
 sky130_fd_sc_hd__o21a_1 \u_cnt/_142_  (.A1(cnt_o[1]),
    .A2(\u_cnt/_097_ ),
    .B1(\u_cnt/_099_ ),
    .X(\u_cnt/_003_ ));
 sky130_fd_sc_hd__xnor2_1 \u_cnt/_143_  (.A(cnt_o[0]),
    .B(\u_cnt/_084_ ),
    .Y(\u_cnt/_100_ ));
 sky130_fd_sc_hd__nand2_1 \u_cnt/_144_  (.A(\u_cnt/_095_ ),
    .B(\u_cnt/_100_ ),
    .Y(\u_cnt/_004_ ));
 sky130_fd_sc_hd__and2_1 \u_cnt/_145_  (.A(cnt_o[20]),
    .B(\u_cnt/_079_ ),
    .X(\u_cnt/_101_ ));
 sky130_fd_sc_hd__o211ai_1 \u_cnt/_146_  (.A1(\u_cnt/_088_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_101_ ),
    .C1(cnt_o[21]),
    .Y(\u_cnt/_102_ ));
 sky130_fd_sc_hd__nand4_1 \u_cnt/_147_  (.A(cnt_o[20]),
    .B(\u_cnt/gate_s2 ),
    .C(\u_cnt/_079_ ),
    .D(\u_cnt/_082_ ),
    .Y(\u_cnt/_103_ ));
 sky130_fd_sc_hd__o21ai_0 \u_cnt/_148_  (.A1(cnt_o[23]),
    .A2(\u_cnt/_103_ ),
    .B1(\u_cnt/_095_ ),
    .Y(\u_cnt/_104_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_149_  (.A1(\u_cnt/_081_ ),
    .A2(\u_cnt/_102_ ),
    .B1(\u_cnt/_104_ ),
    .Y(\u_cnt/_005_ ));
 sky130_fd_sc_hd__o21ai_0 \u_cnt/_150_  (.A1(\u_cnt/_088_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_101_ ),
    .Y(\u_cnt/_105_ ));
 sky130_fd_sc_hd__a31o_1 \u_cnt/_151_  (.A1(cnt_o[21]),
    .A2(\u_cnt/_101_ ),
    .A3(\u_cnt/_084_ ),
    .B1(\u_cnt/_088_ ),
    .X(\u_cnt/_106_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_152_  (.A1(\u_cnt/_080_ ),
    .A2(\u_cnt/_105_ ),
    .B1(\u_cnt/_106_ ),
    .Y(\u_cnt/_006_ ));
 sky130_fd_sc_hd__a21o_1 \u_cnt/_153_  (.A1(\u_cnt/_079_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_088_ ),
    .X(\u_cnt/_026_ ));
 sky130_fd_sc_hd__a31oi_1 \u_cnt/_154_  (.A1(\u_cnt/running ),
    .A2(\u_cnt/_079_ ),
    .A3(\u_cnt/_084_ ),
    .B1(cnt_o[20]),
    .Y(\u_cnt/_027_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_155_  (.A1(cnt_o[20]),
    .A2(\u_cnt/_026_ ),
    .B1(\u_cnt/_027_ ),
    .Y(\u_cnt/_007_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_156_  (.A(cnt_o[19]),
    .Y(\u_cnt/_028_ ));
 sky130_fd_sc_hd__o2111ai_1 \u_cnt/_157_  (.A1(\u_cnt/_088_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_078_ ),
    .C1(cnt_o[17]),
    .D1(cnt_o[18]),
    .Y(\u_cnt/_029_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_158_  (.A1(\u_cnt/_028_ ),
    .A2(\u_cnt/_029_ ),
    .B1(\u_cnt/_026_ ),
    .Y(\u_cnt/_008_ ));
 sky130_fd_sc_hd__nand2_1 \u_cnt/_159_  (.A(cnt_o[17]),
    .B(\u_cnt/_078_ ),
    .Y(\u_cnt/_030_ ));
 sky130_fd_sc_hd__o21ai_0 \u_cnt/_160_  (.A1(\u_cnt/_030_ ),
    .A2(\u_cnt/_096_ ),
    .B1(\u_cnt/_095_ ),
    .Y(\u_cnt/_031_ ));
 sky130_fd_sc_hd__nand2b_1 \u_cnt/_161_  (.A_N(cnt_o[18]),
    .B(\u_cnt/running ),
    .Y(\u_cnt/_032_ ));
 sky130_fd_sc_hd__a31oi_1 \u_cnt/_162_  (.A1(cnt_o[17]),
    .A2(\u_cnt/_078_ ),
    .A3(\u_cnt/_084_ ),
    .B1(cnt_o[18]),
    .Y(\u_cnt/_033_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_163_  (.A1(\u_cnt/_031_ ),
    .A2(\u_cnt/_032_ ),
    .B1(\u_cnt/_033_ ),
    .Y(\u_cnt/_009_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_164_  (.A(cnt_o[17]),
    .Y(\u_cnt/_034_ ));
 sky130_fd_sc_hd__o21ai_0 \u_cnt/_165_  (.A1(\u_cnt/_088_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_078_ ),
    .Y(\u_cnt/_035_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_166_  (.A1(\u_cnt/_034_ ),
    .A2(\u_cnt/_035_ ),
    .B1(\u_cnt/_031_ ),
    .Y(\u_cnt/_010_ ));
 sky130_fd_sc_hd__nor3_1 \u_cnt/_167_  (.A(\u_cnt/_069_ ),
    .B(\u_cnt/_070_ ),
    .C(\u_cnt/_076_ ),
    .Y(\u_cnt/_036_ ));
 sky130_fd_sc_hd__and3_1 \u_cnt/_168_  (.A(cnt_o[13]),
    .B(cnt_o[14]),
    .C(\u_cnt/_036_ ),
    .X(\u_cnt/_037_ ));
 sky130_fd_sc_hd__and3_4 \u_cnt/_169_  (.A(cnt_o[15]),
    .B(\u_cnt/_037_ ),
    .C(\u_cnt/_084_ ),
    .X(\u_cnt/_038_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_170_  (.A1(\u_cnt/_078_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_088_ ),
    .Y(\u_cnt/_039_ ));
 sky130_fd_sc_hd__o21a_1 \u_cnt/_171_  (.A1(cnt_o[16]),
    .A2(\u_cnt/_038_ ),
    .B1(\u_cnt/_039_ ),
    .X(\u_cnt/_011_ ));
 sky130_fd_sc_hd__a41oi_1 \u_cnt/_172_  (.A1(cnt_o[13]),
    .A2(cnt_o[14]),
    .A3(\u_cnt/_036_ ),
    .A4(\u_cnt/_084_ ),
    .B1(cnt_o[15]),
    .Y(\u_cnt/_040_ ));
 sky130_fd_sc_hd__nor3_2 \u_cnt/_173_  (.A(\u_cnt/_088_ ),
    .B(\u_cnt/_038_ ),
    .C(\u_cnt/_040_ ),
    .Y(\u_cnt/_012_ ));
 sky130_fd_sc_hd__nand2_1 \u_cnt/_174_  (.A(\u_cnt/running ),
    .B(\u_cnt/_083_ ),
    .Y(\u_cnt/_041_ ));
 sky130_fd_sc_hd__xnor2_1 \u_cnt/_175_  (.A(tog_o),
    .B(\u_cnt/_041_ ),
    .Y(\u_cnt/_013_ ));
 sky130_fd_sc_hd__and3_4 \u_cnt/_176_  (.A(cnt_o[13]),
    .B(\u_cnt/_036_ ),
    .C(\u_cnt/_084_ ),
    .X(\u_cnt/_042_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_177_  (.A1(\u_cnt/_037_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_088_ ),
    .Y(\u_cnt/_043_ ));
 sky130_fd_sc_hd__o21a_1 \u_cnt/_178_  (.A1(cnt_o[14]),
    .A2(\u_cnt/_042_ ),
    .B1(\u_cnt/_043_ ),
    .X(\u_cnt/_014_ ));
 sky130_fd_sc_hd__a32oi_1 \u_cnt/_179_  (.A1(\u_cnt/running ),
    .A2(\u_cnt/_036_ ),
    .A3(\u_cnt/_084_ ),
    .B1(\u_cnt/_095_ ),
    .B2(cnt_o[13]),
    .Y(\u_cnt/_044_ ));
 sky130_fd_sc_hd__nor2_1 \u_cnt/_180_  (.A(\u_cnt/_042_ ),
    .B(\u_cnt/_044_ ),
    .Y(\u_cnt/_015_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_181_  (.A(cnt_o[23]),
    .Y(\u_cnt/_045_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_182_  (.A1(\u_cnt/_045_ ),
    .A2(\u_cnt/_103_ ),
    .B1(\u_cnt/_088_ ),
    .Y(\u_cnt/_016_ ));
 sky130_fd_sc_hd__nand2_1 \u_cnt/_183_  (.A(cnt_o[8]),
    .B(\u_cnt/_075_ ),
    .Y(\u_cnt/_046_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_184_  (.A(\u_cnt/_046_ ),
    .Y(\u_cnt/_047_ ));
 sky130_fd_sc_hd__and3_1 \u_cnt/_185_  (.A(cnt_o[9]),
    .B(cnt_o[10]),
    .C(\u_cnt/_047_ ),
    .X(\u_cnt/_048_ ));
 sky130_fd_sc_hd__o211ai_1 \u_cnt/_186_  (.A1(\u_cnt/_088_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_048_ ),
    .C1(cnt_o[11]),
    .Y(\u_cnt/_049_ ));
 sky130_fd_sc_hd__a221oi_1 \u_cnt/_187_  (.A1(\u_cnt/_036_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_049_ ),
    .B2(\u_cnt/_070_ ),
    .C1(\u_cnt/_088_ ),
    .Y(\u_cnt/_017_ ));
 sky130_fd_sc_hd__o21ai_0 \u_cnt/_188_  (.A1(\u_cnt/_076_ ),
    .A2(\u_cnt/_096_ ),
    .B1(\u_cnt/_095_ ),
    .Y(\u_cnt/_050_ ));
 sky130_fd_sc_hd__a31oi_1 \u_cnt/_189_  (.A1(\u_cnt/running ),
    .A2(\u_cnt/_048_ ),
    .A3(\u_cnt/_084_ ),
    .B1(cnt_o[11]),
    .Y(\u_cnt/_051_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_190_  (.A1(cnt_o[11]),
    .A2(\u_cnt/_050_ ),
    .B1(\u_cnt/_051_ ),
    .Y(\u_cnt/_018_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_191_  (.A(cnt_o[10]),
    .Y(\u_cnt/_052_ ));
 sky130_fd_sc_hd__o211ai_1 \u_cnt/_192_  (.A1(\u_cnt/_088_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_047_ ),
    .C1(cnt_o[9]),
    .Y(\u_cnt/_053_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_193_  (.A1(\u_cnt/_052_ ),
    .A2(\u_cnt/_053_ ),
    .B1(\u_cnt/_050_ ),
    .Y(\u_cnt/_019_ ));
 sky130_fd_sc_hd__o21ai_0 \u_cnt/_194_  (.A1(\u_cnt/_046_ ),
    .A2(\u_cnt/_096_ ),
    .B1(\u_cnt/_095_ ),
    .Y(\u_cnt/_054_ ));
 sky130_fd_sc_hd__nand2b_1 \u_cnt/_195_  (.A_N(cnt_o[9]),
    .B(\u_cnt/running ),
    .Y(\u_cnt/_055_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_196_  (.A1(\u_cnt/_047_ ),
    .A2(\u_cnt/_084_ ),
    .B1(cnt_o[9]),
    .Y(\u_cnt/_056_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_197_  (.A1(\u_cnt/_054_ ),
    .A2(\u_cnt/_055_ ),
    .B1(\u_cnt/_056_ ),
    .Y(\u_cnt/_020_ ));
 sky130_fd_sc_hd__inv_1 \u_cnt/_198_  (.A(cnt_o[8]),
    .Y(\u_cnt/_057_ ));
 sky130_fd_sc_hd__o21ai_0 \u_cnt/_199_  (.A1(\u_cnt/_088_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_075_ ),
    .Y(\u_cnt/_058_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_200_  (.A1(\u_cnt/_057_ ),
    .A2(\u_cnt/_058_ ),
    .B1(\u_cnt/_054_ ),
    .Y(\u_cnt/_021_ ));
 sky130_fd_sc_hd__nor2_1 \u_cnt/_201_  (.A(\u_cnt/_073_ ),
    .B(\u_cnt/_074_ ),
    .Y(\u_cnt/_059_ ));
 sky130_fd_sc_hd__nand2_1 \u_cnt/_202_  (.A(cnt_o[6]),
    .B(\u_cnt/_059_ ),
    .Y(\u_cnt/_060_ ));
 sky130_fd_sc_hd__o21ai_0 \u_cnt/_203_  (.A1(\u_cnt/_060_ ),
    .A2(\u_cnt/_096_ ),
    .B1(\u_cnt/_095_ ),
    .Y(\u_cnt/_061_ ));
 sky130_fd_sc_hd__nand2_1 \u_cnt/_204_  (.A(\u_cnt/_072_ ),
    .B(\u_cnt/running ),
    .Y(\u_cnt/_062_ ));
 sky130_fd_sc_hd__a31oi_1 \u_cnt/_205_  (.A1(cnt_o[6]),
    .A2(\u_cnt/_059_ ),
    .A3(\u_cnt/_084_ ),
    .B1(cnt_o[7]),
    .Y(\u_cnt/_063_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_206_  (.A1(\u_cnt/_061_ ),
    .A2(\u_cnt/_062_ ),
    .B1(\u_cnt/_063_ ),
    .Y(\u_cnt/_022_ ));
 sky130_fd_sc_hd__o21ai_0 \u_cnt/_207_  (.A1(\u_cnt/_088_ ),
    .A2(\u_cnt/_084_ ),
    .B1(\u_cnt/_059_ ),
    .Y(\u_cnt/_064_ ));
 sky130_fd_sc_hd__a21oi_1 \u_cnt/_208_  (.A1(\u_cnt/_071_ ),
    .A2(\u_cnt/_064_ ),
    .B1(\u_cnt/_061_ ),
    .Y(\u_cnt/_023_ ));
 sky130_fd_sc_hd__nor2b_1 \u_cnt/_209_  (.A(cnt_o[5]),
    .B_N(\u_cnt/running ),
    .Y(\u_cnt/_065_ ));
 sky130_fd_sc_hd__a41o_1 \u_cnt/_210_  (.A1(cnt_o[3]),
    .A2(cnt_o[4]),
    .A3(\u_cnt/_068_ ),
    .A4(\u_cnt/_084_ ),
    .B1(cnt_o[5]),
    .X(\u_cnt/_066_ ));
 sky130_fd_sc_hd__o21a_1 \u_cnt/_211_  (.A1(\u_cnt/_090_ ),
    .A2(\u_cnt/_065_ ),
    .B1(\u_cnt/_066_ ),
    .X(\u_cnt/_024_ ));
 sky130_fd_sc_hd__a41oi_1 \u_cnt/_212_  (.A1(cnt_o[23]),
    .A2(\u_cnt/gate_s2 ),
    .A3(\u_cnt/_101_ ),
    .A4(\u_cnt/_082_ ),
    .B1(ovf_o),
    .Y(\u_cnt/_067_ ));
 sky130_fd_sc_hd__nor2_1 \u_cnt/_213_  (.A(\u_cnt/_088_ ),
    .B(\u_cnt/_067_ ),
    .Y(\u_cnt/_025_ ));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_214_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_004_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[0]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_215_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_003_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[1]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_216_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_002_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[2]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_217_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_001_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[3]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_218_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_000_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[4]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_219_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_024_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[5]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_220_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_023_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[6]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_221_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_022_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[7]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_222_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_021_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[8]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_223_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_020_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[9]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_224_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_019_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[10]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_225_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_018_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[11]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_226_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_017_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[12]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_227_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_015_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[13]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_228_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_014_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[14]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_229_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_012_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[15]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_230_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_011_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[16]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_231_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_010_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[17]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_232_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_009_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[18]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_233_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_008_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[19]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_234_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_007_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[20]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_235_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_006_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[21]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_236_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_005_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[22]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_237_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_016_ ),
    .RESET_B(rst_n),
    .Q(cnt_o[23]));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_238_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_013_ ),
    .RESET_B(rst_n),
    .Q(tog_o));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_239_  (.CLK(osc_sel_clk),
    .D(\u_cnt/_025_ ),
    .RESET_B(rst_n),
    .Q(ovf_o));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_240_  (.CLK(osc_sel_clk),
    .D(gate_en),
    .RESET_B(rst_n),
    .Q(\u_cnt/gate_s1 ));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_241_  (.CLK(osc_sel_clk),
    .D(\u_cnt/gate_s1 ),
    .RESET_B(rst_n),
    .Q(\u_cnt/gate_s2 ));
 sky130_fd_sc_hd__dfrtp_1 \u_cnt/_242_  (.CLK(osc_sel_clk),
    .D(\u_cnt/gate_s2 ),
    .RESET_B(rst_n),
    .Q(\u_cnt/running ));
 assign busy = busy_r;
 assign done = done_r;
 assign overflow = ovf_r;
endmodule
